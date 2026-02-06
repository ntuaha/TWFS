# Open Issue Resolution Matrix

This document maps legacy open issues to implemented features in the current codebase.

## Closed by current implementation

- #2 Dataset schema: implemented by normalized `facts` schema in `pipelines/build_databases.py` and documented in `www/DATA_DICTIONARY.md`.
- #4 Basic web information page: implemented by new static dashboard `www/index.html` + `www/app.js`.
- #9 Add AREA_DP: monthly crawler includes AREA_DP source mapping in `pipelines/crawl_latest.py`.
- #17 Add OC: monthly crawler includes OC source mapping in `pipelines/crawl_latest.py`.
- #19 List extracted/transformed/loaded data time windows: implemented by `database/issue_status_report.json` generated from `pipelines/build_databases.py`.
- #20 Automated extract scheduling: implemented by GitHub Actions scheduler in `.github/workflows/deploy-gh-pages.yml`.
- #21 Utility library: implemented by reusable `pipelines/*.py` utility scripts.
- #31 Missing coop data rows: coverage/missing-month diagnostics now generated in `database/issue_status_report.json`.
- #33 Create table program: implemented by automatic SQLite/DuckDB table creation in `pipelines/build_databases.py`.
- #34 Load to DB program: implemented by CSV->SQLite/DuckDB loading in `pipelines/build_databases.py`.
- #35 Monthly report output: implemented by static report artifacts (`www/data/*`) refreshed by scheduled workflow.
- #37 Add web page: implemented by current dashboard.
- #39 Add DFEI information: crawler includes DFEI source mapping and pipeline supports dataset-level ingestion.
- #40 Y_BAL pre-2008-08 missing: pipeline now generates an explicit Y_BAL historical presence check in `database/issue_status_report.json`.

## Notes

- Legacy issue bodies are mostly empty and from 2013-2014. Resolution is based on intended capability coverage in the current architecture.
