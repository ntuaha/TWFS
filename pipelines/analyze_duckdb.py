#!/usr/bin/env python3
"""DuckDB analysis helper for TWFS."""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze TWFS via DuckDB")
    parser.add_argument("--db", default="database/twfs.duckdb", help="DuckDB path")
    parser.add_argument("--query", help="Custom SQL query")
    parser.add_argument(
        "--top-institutions",
        action="store_true",
        help="Show top institutions by total value_num",
    )
    parser.add_argument(
        "--month", help="Month key filter (YYYY-MM), used with --top-institutions"
    )
    parser.add_argument("--limit", type=int, default=20)
    return parser.parse_args()


def print_rows(rows: list[tuple], columns: list[str]) -> None:
    print("\t".join(columns))
    for row in rows:
        print("\t".join("" if v is None else str(v) for v in row))


def main() -> None:
    args = parse_args()
    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"DuckDB file not found: {db_path}")

    conn = duckdb.connect(str(db_path))

    if args.query:
        sql = args.query
    elif args.top_institutions:
        where = "WHERE value_num IS NOT NULL"
        params: list[str] = []
        if args.month:
            where += " AND month_key = ?"
            params.append(args.month)
        sql = (
            "SELECT institution, ROUND(SUM(value_num), 2) AS total_value "
            "FROM facts "
            f"{where} "
            "GROUP BY institution "
            "ORDER BY total_value DESC "
            f"LIMIT {args.limit}"
        )
        result = conn.execute(sql, params)
        print_rows(result.fetchall(), [c[0] for c in result.description])
        return
    else:
        sql = (
            "SELECT month_key, COUNT(*) AS row_count, ROUND(SUM(value_num), 2) AS total_value "
            "FROM facts "
            "GROUP BY month_key "
            "ORDER BY month_key DESC "
            f"LIMIT {args.limit}"
        )

    result = conn.execute(sql)
    print_rows(result.fetchall(), [c[0] for c in result.description])


if __name__ == "__main__":
    main()
