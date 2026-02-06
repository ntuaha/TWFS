#!/usr/bin/env python3
"""Download latest available TWFS files.

Default source is the new FSC OpenAPI CSV endpoint.
Legacy survey.banking.gov.tw crawling is kept for compatibility.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import ssl
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class OpenAPISource:
    dataset: str
    table_id: str


@dataclass(frozen=True)
class LegacySource:
    dataset: str
    category_idx: str
    file_code: str


OPENAPI_SOURCES: list[OpenAPISource] = [
    OpenAPISource("FSC_B01", "B01"),
    OpenAPISource("FSC_B02", "B02"),
    OpenAPISource("FSC_B03", "B03"),
    OpenAPISource("FSC_B04", "B04"),
    OpenAPISource("FSC_B05", "B05"),
    OpenAPISource("FSC_B06", "B06"),
    OpenAPISource("FSC_B07", "B07"),
    OpenAPISource("FSC_B08", "B08"),
    OpenAPISource("FSC_B09", "B09"),
    OpenAPISource("FSC_B10", "B10"),
    OpenAPISource("FSC_B11", "B11"),
    OpenAPISource("FSC_B12", "B12"),
    OpenAPISource("FSC_B13", "B13"),
    OpenAPISource("FSC_B14", "B14"),
]
OPENAPI_DISCOVERY_URL = (
    "https://stat.fsc.gov.tw/FSCChartShow_Restore/CRPages/MS_Chart_Show.aspx?Beauid=Banking"
)

LEGACY_SOURCES: list[LegacySource] = [
    LegacySource("DFEI", "4_1", "4140"),
    LegacySource("MD_BAL", "2_1", "22010"),
    LegacySource("MD_AUM", "2_1", "22020"),
    LegacySource("FD_BAL", "2_1", "22030"),
    LegacySource("NC", "2_1", "22040"),
    LegacySource("Y_BAL", "2_1", "22050"),
    LegacySource("CD", "2_1", "22060"),
    LegacySource("AREA_DP", "2_1", "213010"),
    LegacySource("CC", "2_1", "29010"),
    LegacySource("ATM", "2_1", "28010"),
    LegacySource("OC", "2_1", "21020"),
    LegacySource("PFEI", "2_1", "21010"),
    LegacySource("LPPE", "2_1", "24030"),
    LegacySource("LSME", "2_1", "24040"),
    LegacySource("LN", "2_1", "24010"),
    LegacySource("LN_AUM", "2_1", "24020"),
    LegacySource("CL", "2_1", "25010"),
    LegacySource("CL_INFO", "2_1", "25020"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl latest TWFS files")
    parser.add_argument("--base-path", default=".", help="Repository base path")
    parser.add_argument("--lookback-months", type=int, default=24)
    parser.add_argument(
        "--source",
        choices=["openapi", "legacy", "both"],
        default="openapi",
        help="Data source mode; default is new OpenAPI source",
    )
    parser.add_argument(
        "--data-type",
        type=int,
        default=1,
        help="OpenAPI DATA_TYPE (1=monthly, 2=yearly)",
    )
    return parser.parse_args()


def fetch_bytes(url: str, timeout: int = 60) -> bytes:
    req = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
        },
        method="GET",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except ssl.SSLError:
        # Some FSC hosts intermittently serve a certificate chain that fails strict
        # verification in CI runners. Retry with an unverified context for resilience.
        unverified = ssl._create_unverified_context()
        with urlopen(req, timeout=timeout, context=unverified) as resp:
            return resp.read()
    except URLError as exc:
        if isinstance(exc.reason, ssl.SSLError):
            unverified = ssl._create_unverified_context()
            with urlopen(req, timeout=timeout, context=unverified) as resp:
                return resp.read()
        raise


def detect_latest_token(csv_bytes: bytes) -> str | None:
    text = csv_bytes.decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text))

    latest = None
    for idx, row in enumerate(reader):
        if idx == 0 or not row:
            continue
        token = "".join(ch for ch in str(row[0]).strip() if ch.isdigit())
        if len(token) < 4:
            continue
        if latest is None or token > latest:
            latest = token
    return latest


def discover_openapi_sources() -> list[OpenAPISource]:
    try:
        html = fetch_bytes(OPENAPI_DISCOVERY_URL, timeout=30).decode(
            "utf-8-sig", errors="replace"
        )
        table_ids = sorted(
            set(re.findall(r'<option value="(B\\d{2})">', html)),
            key=lambda x: int(x[1:]),
        )
        if table_ids:
            return [OpenAPISource(f"FSC_{tid}", tid) for tid in table_ids]
    except Exception:
        pass
    return OPENAPI_SOURCES


def crawl_openapi(base_path: Path, data_type: int, openapi_sources: list[OpenAPISource]) -> list[dict]:
    output_dir = base_path / "rawdata" / "openapi"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for src in openapi_sources:
        params = urlencode(
            {"DATA_TYPE": data_type, "TableID": src.table_id, "OUTPUT_FILE": "Y"}
        )
        url = f"https://stat.fsc.gov.tw/FSC_OAS3_RESTORE/api/CSV_EXPORT?{params}"
        out_path = output_dir / f"{src.table_id}.csv"

        record = {
            "source": "openapi",
            "dataset": src.dataset,
            "table_id": src.table_id,
            "status": "missing",
            "url": url,
            "saved_to": str(out_path),
            "latest_token": None,
            "sha256": None,
        }

        try:
            data = fetch_bytes(url)
            latest = detect_latest_token(data)
            digest = hashlib.sha256(data).hexdigest()

            record["latest_token"] = latest
            record["sha256"] = digest

            if out_path.exists() and out_path.read_bytes() == data:
                record["status"] = "exists"
            else:
                out_path.write_bytes(data)
                record["status"] = "downloaded"
        except (HTTPError, URLError) as exc:
            record["status"] = f"error: {exc}"
        except Exception as exc:  # pragma: no cover
            record["status"] = f"error: {exc}"

        results.append(record)

    return results


def subtract_months(year: int, month: int, delta: int) -> tuple[int, int]:
    total = year * 12 + (month - 1) - delta
    new_year = total // 12
    new_month = (total % 12) + 1
    return new_year, new_month


def candidate_roc_months(lookback_months: int) -> list[tuple[int, int]]:
    today = date.today()
    out = []
    for i in range(lookback_months):
        y, m = subtract_months(today.year, today.month, i)
        out.append((y - 1911, m))
    return out


def build_legacy_url(src: LegacySource, roc_year: int, month: int) -> str:
    ym = f"{roc_year}{month:02d}"
    return f"https://survey.banking.gov.tw/statis/{src.category_idx}_{ym}{ym}/{src.file_code}.xls"


def is_available(url: str, timeout: int = 20) -> bool:
    req = Request(url, method="HEAD")
    try:
        with urlopen(req, timeout=timeout):
            return True
    except HTTPError as exc:
        if exc.code in {403, 405}:
            try:
                with urlopen(Request(url, method="GET"), timeout=timeout):
                    return True
            except Exception:
                return False
        return False
    except URLError:
        return False


def crawl_legacy(base_path: Path, lookback_months: int) -> list[dict]:
    rawdata = base_path / "rawdata"
    results = []
    candidates = candidate_roc_months(lookback_months)

    for src in LEGACY_SOURCES:
        record = {
            "source": "legacy",
            "dataset": src.dataset,
            "status": "missing",
            "url": None,
            "saved_to": None,
            "latest_token": None,
        }

        found = None
        for roc_year, month in candidates:
            url = build_legacy_url(src, roc_year, month)
            if is_available(url):
                found = (roc_year, month, url)
                break

        if found is None:
            results.append(record)
            continue

        roc_year, month, url = found
        roc_ym = f"{roc_year}{month:02d}"
        out_path = rawdata / src.dataset / f"{roc_ym}.xls"

        record["url"] = url
        record["saved_to"] = str(out_path)
        record["latest_token"] = roc_ym

        try:
            data = fetch_bytes(url)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if out_path.exists() and out_path.read_bytes() == data:
                record["status"] = "exists"
            else:
                out_path.write_bytes(data)
                record["status"] = "downloaded"
        except Exception as exc:  # pragma: no cover
            record["status"] = f"error: {exc}"

        results.append(record)

    return results


def summarize(sources: list[dict]) -> dict:
    downloaded = sum(1 for s in sources if s["status"] == "downloaded")
    existed = sum(1 for s in sources if s["status"] == "exists")
    missing = sum(1 for s in sources if s["status"] == "missing")
    errors = sum(1 for s in sources if str(s["status"]).startswith("error:"))
    return {
        "downloaded": downloaded,
        "exists": existed,
        "missing": missing,
        "errors": errors,
        "total": len(sources),
    }


def main() -> None:
    args = parse_args()
    base_path = Path(args.base_path).resolve()

    manifest = {
        "generated_at": date.today().isoformat(),
        "mode": args.source,
        "openapi_data_type": args.data_type,
        "lookback_months": args.lookback_months,
        "sources": [],
        "summary": {},
    }

    if args.source in {"openapi", "both"}:
        openapi_sources = discover_openapi_sources()
        manifest["openapi_table_count"] = len(openapi_sources)
        manifest["openapi_table_ids"] = [s.table_id for s in openapi_sources]
        manifest["sources"].extend(crawl_openapi(base_path, args.data_type, openapi_sources))
    if args.source in {"legacy", "both"}:
        manifest["sources"].extend(crawl_legacy(base_path, args.lookback_months))

    manifest["summary"] = summarize(manifest["sources"])

    output = base_path / "database" / "crawl_manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Mode: {args.source}")
    print(f"Downloaded: {manifest['summary']['downloaded']}")
    print(f"Already exists: {manifest['summary']['exists']}")
    print(f"Missing: {manifest['summary']['missing']}")
    print(f"Errors: {manifest['summary']['errors']}")
    print(f"Manifest: {output}")


if __name__ == "__main__":
    main()
