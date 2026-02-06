#!/usr/bin/env python3
"""Download latest available monthly XLS files from the TWFS source."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Source:
    dataset: str
    category_idx: str
    file_code: str


SOURCES: list[Source] = [
    Source("DFEI", "4_1", "4140"),
    Source("MD_BAL", "2_1", "22010"),
    Source("MD_AUM", "2_1", "22020"),
    Source("FD_BAL", "2_1", "22030"),
    Source("NC", "2_1", "22040"),
    Source("Y_BAL", "2_1", "22050"),
    Source("CD", "2_1", "22060"),
    Source("AREA_DP", "2_1", "213010"),
    Source("CC", "2_1", "29010"),
    Source("ATM", "2_1", "28010"),
    Source("OC", "2_1", "21020"),
    Source("PFEI", "2_1", "21010"),
    Source("LPPE", "2_1", "24030"),
    Source("LSME", "2_1", "24040"),
    Source("LN", "2_1", "24010"),
    Source("LN_AUM", "2_1", "24020"),
    Source("CL", "2_1", "25010"),
    Source("CL_INFO", "2_1", "25020"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl latest TWFS XLS files")
    parser.add_argument("--base-path", default=".", help="Repository base path")
    parser.add_argument("--lookback-months", type=int, default=24)
    return parser.parse_args()


def subtract_months(year: int, month: int, delta: int) -> tuple[int, int]:
    total = year * 12 + (month - 1) - delta
    new_year = total // 12
    new_month = (total % 12) + 1
    return new_year, new_month


def candidate_roc_months(lookback_months: int) -> list[tuple[int, int]]:
    today = date.today()
    ad_year = today.year
    ad_month = today.month

    out = []
    for i in range(lookback_months):
        y, m = subtract_months(ad_year, ad_month, i)
        roc_year = y - 1911
        out.append((roc_year, m))
    return out


def build_url(src: Source, roc_year: int, month: int) -> str:
    ym = f"{roc_year}{month:02d}"
    return (
        f"https://survey.banking.gov.tw/statis/{src.category_idx}_{ym}{ym}/{src.file_code}.xls"
    )


def is_available(url: str, timeout: int = 20) -> bool:
    req = Request(url, method="HEAD")
    try:
        with urlopen(req, timeout=timeout):
            return True
    except HTTPError as exc:
        if exc.code in {405, 403}:
            try:
                with urlopen(Request(url, method="GET"), timeout=timeout):
                    return True
            except Exception:
                return False
        return False
    except URLError:
        return False


def download(url: str, out_path: Path, timeout: int = 60) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
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
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    out_path.write_bytes(data)


def main() -> None:
    args = parse_args()
    base_path = Path(args.base_path).resolve()
    rawdata = base_path / "rawdata"

    manifest = {
        "generated_at": date.today().isoformat(),
        "lookback_months": args.lookback_months,
        "sources": [],
    }

    candidates = candidate_roc_months(args.lookback_months)

    for src in SOURCES:
        record = {
            "dataset": src.dataset,
            "status": "missing",
            "url": None,
            "saved_to": None,
            "roc_ym": None,
        }

        found = None
        for roc_year, month in candidates:
            url = build_url(src, roc_year, month)
            if is_available(url):
                found = (roc_year, month, url)
                break

        if found is None:
            manifest["sources"].append(record)
            continue

        roc_year, month, url = found
        roc_ym = f"{roc_year}{month:02d}"
        out_path = rawdata / src.dataset / f"{roc_ym}.xls"

        record["url"] = url
        record["saved_to"] = str(out_path)
        record["roc_ym"] = roc_ym

        if out_path.exists() and out_path.stat().st_size > 1024:
            record["status"] = "exists"
        else:
            try:
                download(url, out_path)
                record["status"] = "downloaded"
            except Exception as exc:  # pragma: no cover - operational safeguard
                record["status"] = f"error: {exc}"

        manifest["sources"].append(record)

    output = base_path / "database" / "crawl_manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    downloaded = sum(1 for s in manifest["sources"] if s["status"] == "downloaded")
    existed = sum(1 for s in manifest["sources"] if s["status"] == "exists")
    missing = sum(1 for s in manifest["sources"] if s["status"] == "missing")

    print(f"Downloaded: {downloaded}")
    print(f"Already exists: {existed}")
    print(f"Missing: {missing}")
    print(f"Manifest: {output}")


if __name__ == "__main__":
    main()
