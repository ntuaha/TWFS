#!/usr/bin/env python3
"""Build SQLite + DuckDB databases and static web JSON from TWFS CSV files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass
class FactRow:
    dataset: str
    roc_ym: str
    ad_year: int
    month: int
    month_key: str
    institution: str
    institution_type: str
    item_zh: str
    item_en: str
    value_raw: str
    value_num: float | None
    source_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build TWFS databases and web assets")
    parser.add_argument("--base-path", default=".", help="Repository base path")
    parser.add_argument(
        "--sqlite-path", default="database/twfs.sqlite", help="SQLite output path"
    )
    parser.add_argument(
        "--duckdb-path", default="database/twfs.duckdb", help="DuckDB output path"
    )
    parser.add_argument(
        "--web-data-dir", default="www/data", help="Static web data output directory"
    )
    parser.add_argument(
        "--status-report-path",
        default="database/issue_status_report.json",
        help="Issue/coverage status report JSON output path",
    )
    parser.add_argument(
        "--skip-duckdb",
        action="store_true",
        help="Skip DuckDB build (useful for offline/local env without duckdb package)",
    )
    return parser.parse_args()


def parse_roc_ym(raw: str) -> tuple[str, int, int, str] | None:
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) < 4:
        return None

    month = int(digits[-2:])
    if month < 1 or month > 12:
        return None

    roc_year = int(digits[:-2])
    ad_year = roc_year + 1911
    month_key = f"{ad_year:04d}-{month:02d}"
    return digits, ad_year, month, month_key


def parse_any_ym(raw: str) -> tuple[str, int, int, str] | None:
    s = (raw or "").strip()
    if not s:
        return None

    if "/" in s:
        parts = s.split("/")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            y = int(parts[0])
            m = int(parts[1])
            if y >= 1900 and 1 <= m <= 12:
                token = f"{y:04d}{m:02d}"
                return token, y, m, f"{y:04d}-{m:02d}"

    digits = "".join(ch for ch in s if ch.isdigit())
    if not digits:
        return None

    if len(digits) == 6:
        y = int(digits[:4])
        m = int(digits[-2:])
        if y >= 1900 and 1 <= m <= 12:
            return digits, y, m, f"{y:04d}-{m:02d}"

    if len(digits) == 4:
        y = int(digits)
        if y >= 1900:
            return digits, y, 1, f"{y:04d}-01"

    return parse_roc_ym(raw)


def parse_value(raw: str) -> float | None:
    val = raw.strip().replace(",", "")
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        return None


def read_facts(data_dir: Path) -> list[FactRow]:
    rows: list[FactRow] = []
    for csv_path in sorted(data_dir.glob("*/*.csv")):
        dataset = csv_path.parent.name
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for rec in reader:
                ym_raw = (rec.get("年月") or "").strip()
                ym_parsed = parse_roc_ym(ym_raw)
                if ym_parsed is None:
                    continue

                roc_ym, ad_year, month, month_key = ym_parsed
                value_raw = (rec.get("數值") or "").strip()
                item_en = (rec.get("英文欄位") or rec.get("英文項目") or "").strip()

                rows.append(
                    FactRow(
                        dataset=dataset,
                        roc_ym=roc_ym,
                        ad_year=ad_year,
                        month=month,
                        month_key=month_key,
                        institution=(rec.get("銀行") or "").strip(),
                        institution_type=(rec.get("銀行類別") or "").strip(),
                        item_zh=(rec.get("項目") or "").strip(),
                        item_en=item_en,
                        value_raw=value_raw,
                        value_num=parse_value(value_raw),
                        source_file=str(csv_path),
                    )
                )
    return rows


def read_openapi_facts(openapi_dir: Path) -> list[FactRow]:
    rows: list[FactRow] = []
    if not openapi_dir.exists():
        return rows

    for csv_path in sorted(openapi_dir.glob("*.csv")):
        dataset = f"OPENAPI_{csv_path.stem}"
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                continue

            metric_cols = [
                c for c in reader.fieldnames if c not in {"年月", "公告日期", "TRANS_DATE"}
            ]
            for rec in reader:
                ym_parsed = parse_any_ym(rec.get("年月", ""))
                if ym_parsed is None:
                    continue
                token, ad_year, month, month_key = ym_parsed

                for metric in metric_cols:
                    value_raw = (rec.get(metric) or "").strip()
                    if value_raw == "":
                        continue
                    rows.append(
                        FactRow(
                            dataset=dataset,
                            roc_ym=token,
                            ad_year=ad_year,
                            month=month,
                            month_key=month_key,
                            institution="總計",
                            institution_type="OpenAPI",
                            item_zh=metric,
                            item_en=metric,
                            value_raw=value_raw,
                            value_num=parse_value(value_raw),
                            source_file=str(csv_path),
                        )
                    )
    return rows


def create_sqlite(sqlite_path: Path, rows: Iterable[FactRow]) -> None:
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS facts;
        CREATE TABLE facts (
            dataset TEXT NOT NULL,
            roc_ym TEXT NOT NULL,
            ad_year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            month_key TEXT NOT NULL,
            institution TEXT NOT NULL,
            institution_type TEXT NOT NULL,
            item_zh TEXT NOT NULL,
            item_en TEXT NOT NULL,
            value_raw TEXT NOT NULL,
            value_num REAL,
            source_file TEXT NOT NULL,
            UNIQUE (dataset, roc_ym, institution, institution_type, item_zh, item_en, source_file)
        );
        CREATE INDEX idx_facts_month_key ON facts(month_key);
        CREATE INDEX idx_facts_institution ON facts(institution);
        CREATE INDEX idx_facts_dataset ON facts(dataset);
        CREATE INDEX idx_facts_item_en ON facts(item_en);
        """
    )

    cur.executemany(
        """
        INSERT OR REPLACE INTO facts (
            dataset, roc_ym, ad_year, month, month_key,
            institution, institution_type, item_zh, item_en,
            value_raw, value_num, source_file
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                r.dataset,
                r.roc_ym,
                r.ad_year,
                r.month,
                r.month_key,
                r.institution,
                r.institution_type,
                r.item_zh,
                r.item_en,
                r.value_raw,
                r.value_num,
                r.source_file,
            )
            for r in rows
        ],
    )

    conn.commit()
    conn.close()


def create_duckdb(duckdb_path: Path, rows: Iterable[FactRow]) -> bool:
    try:
        import duckdb
    except ModuleNotFoundError as exc:
        print("duckdb module not found. Skip DuckDB build.")
        return False

    duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(duckdb_path))

    conn.execute("DROP TABLE IF EXISTS facts")
    conn.execute(
        """
        CREATE TABLE facts (
            dataset VARCHAR,
            roc_ym VARCHAR,
            ad_year INTEGER,
            month INTEGER,
            month_key VARCHAR,
            institution VARCHAR,
            institution_type VARCHAR,
            item_zh VARCHAR,
            item_en VARCHAR,
            value_raw VARCHAR,
            value_num DOUBLE,
            source_file VARCHAR
        )
        """
    )

    conn.executemany(
        """
        INSERT INTO facts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                r.dataset,
                r.roc_ym,
                r.ad_year,
                r.month,
                r.month_key,
                r.institution,
                r.institution_type,
                r.item_zh,
                r.item_en,
                r.value_raw,
                r.value_num,
                r.source_file,
            )
            for r in rows
        ],
    )

    conn.close()
    return True


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )


def get_institution_filename(name: str) -> str:
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()[:16]
    return f"inst_{digest}.json"


def export_web_json(sqlite_path: Path, web_data_dir: Path) -> None:
    by_month_dir = web_data_dir / "by_month"
    by_inst_dir = web_data_dir / "by_institution"
    by_month_dir.mkdir(parents=True, exist_ok=True)
    by_inst_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row

    months = [
        r[0]
        for r in conn.execute("SELECT DISTINCT month_key FROM facts ORDER BY month_key").fetchall()
    ]
    institutions = [
        r[0]
        for r in conn.execute(
            "SELECT DISTINCT institution FROM facts WHERE institution <> '' ORDER BY institution"
        ).fetchall()
    ]
    datasets = [
        r[0] for r in conn.execute("SELECT DISTINCT dataset FROM facts ORDER BY dataset").fetchall()
    ]

    for month in months:
        recs = [
            dict(r)
            for r in conn.execute(
                """
                SELECT dataset, month_key, institution, institution_type, item_zh, item_en, value_num, value_raw
                FROM facts WHERE month_key = ?
                ORDER BY dataset, institution, item_en, item_zh
                """,
                (month,),
            ).fetchall()
        ]
        write_json(by_month_dir / f"{month}.json", recs)

    institution_index = []
    for inst in institutions:
        filename = get_institution_filename(inst)
        institution_index.append({"name": inst, "file": filename})
        recs = [
            dict(r)
            for r in conn.execute(
                """
                SELECT dataset, month_key, institution, institution_type, item_zh, item_en, value_num, value_raw
                FROM facts WHERE institution = ?
                ORDER BY month_key, dataset, item_en, item_zh
                """,
                (inst,),
            ).fetchall()
        ]
        write_json(by_inst_dir / filename, recs)

    total_rows = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]

    catalog = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "months": months,
        "institutions": institution_index,
        "datasets": datasets,
        "row_count": total_rows,
    }
    write_json(web_data_dir / "catalog.json", catalog)

    conn.close()


def month_range(start: str, end: str) -> list[str]:
    sy, sm = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    out = []
    y, m = sy, sm
    while (y, m) <= (ey, em):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            y += 1
            m = 1
    return out


def export_issue_status(sqlite_path: Path, output_path: Path) -> None:
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row

    row = conn.execute(
        "SELECT MIN(month_key) AS min_month, MAX(month_key) AS max_month FROM facts"
    ).fetchone()
    min_month = row["min_month"]
    max_month = row["max_month"]
    expected = month_range(min_month, max_month)

    datasets = [
        r[0] for r in conn.execute("SELECT DISTINCT dataset FROM facts ORDER BY dataset").fetchall()
    ]
    coverage = []
    for ds in datasets:
        months = [
            r[0]
            for r in conn.execute(
                "SELECT DISTINCT month_key FROM facts WHERE dataset = ? ORDER BY month_key", (ds,)
            ).fetchall()
        ]
        month_set = set(months)
        missing = [m for m in expected if m not in month_set]
        r = conn.execute(
            """
            SELECT COUNT(*) AS row_count, MIN(month_key) AS min_month, MAX(month_key) AS max_month
            FROM facts WHERE dataset = ?
            """,
            (ds,),
        ).fetchone()
        coverage.append(
            {
                "dataset": ds,
                "row_count": r["row_count"],
                "min_month": r["min_month"],
                "max_month": r["max_month"],
                "months_available": len(months),
                "missing_months_count": len(missing),
                "missing_months": missing,
            }
        )

    y_bal_pre_cutoff = conn.execute(
        """
        SELECT COUNT(*) FROM facts
        WHERE dataset = 'Y_BAL' AND month_key < '2008-08'
        """
    ).fetchone()[0]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "month_window": {"min": min_month, "max": max_month},
        "dataset_coverage": coverage,
        "checks": {
            "y_bal_pre_2008_08_row_count": y_bal_pre_cutoff,
            "y_bal_pre_2008_08_has_data": y_bal_pre_cutoff > 0,
        },
    }
    write_json(output_path, report)
    conn.close()


def main() -> None:
    args = parse_args()
    base_path = Path(args.base_path).resolve()
    data_dir = base_path / "data"
    openapi_dir = base_path / "rawdata" / "openapi"

    rows = read_facts(data_dir)
    rows.extend(read_openapi_facts(openapi_dir))
    if not rows:
        raise SystemExit(f"No CSV rows found under {data_dir}")

    sqlite_path = (base_path / args.sqlite_path).resolve()
    duckdb_path = (base_path / args.duckdb_path).resolve()
    web_data_dir = (base_path / args.web_data_dir).resolve()
    status_report_path = (base_path / args.status_report_path).resolve()

    create_sqlite(sqlite_path, rows)
    duckdb_built = False
    if not args.skip_duckdb:
        duckdb_built = create_duckdb(duckdb_path, rows)
    export_web_json(sqlite_path, web_data_dir)
    export_issue_status(sqlite_path, status_report_path)

    print(f"Built SQLite: {sqlite_path}")
    if args.skip_duckdb:
        print("Skipped DuckDB by option: --skip-duckdb")
    elif duckdb_built:
        print(f"Built DuckDB: {duckdb_path}")
    else:
        print("DuckDB was not built in this environment.")
    print(f"Exported web JSON under: {web_data_dir}")
    print(f"Exported issue status report: {status_report_path}")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    main()
