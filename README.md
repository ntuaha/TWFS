# 台灣金融統計 (TWFS)

此專案提供一套可自動化執行的資料流程：

- 從既有 `data/*/*.csv` 建立 `SQLite` 與 `DuckDB` 分析資料庫
- 產生可部署到 `gh-pages` 的靜態網頁資料（按月、按機構）
- 定期執行爬蟲下載最新月的原始 `xls`
- 透過 GitHub Actions 自動建置與部署

## 網站

- GitHub Pages: https://ntuaha.github.io/TWFS/

## 目錄

- `/pipelines/build_databases.py`：CSV -> SQLite + DuckDB + `www/data/*`
- `/pipelines/crawl_latest.py`：下載各資料集最新可得月份的 `xls`
- `/pipelines/analyze_duckdb.py`：DuckDB 查詢工具
- `/www/index.html`：靜態儀表板（逐月 / 逐機構）
- `/www/DATA_DICTIONARY.md`：資料欄位定義

## 本機執行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python pipelines/build_databases.py --base-path .
python pipelines/analyze_duckdb.py --top-institutions --month 2011-01 --limit 10
```

輸出：

- SQLite: `database/twfs.sqlite`
- DuckDB: `database/twfs.duckdb`
- Web data: `www/data/catalog.json`、`www/data/by_month/*`、`www/data/by_institution/*`

## 定期更新資料

```bash
python pipelines/crawl_latest.py --base-path .
python pipelines/build_databases.py --base-path .
```

## GitHub Actions / gh-pages

已提供 workflow：

- `/.github/workflows/ci.yml`
- `/.github/workflows/deploy-gh-pages.yml`

啟用方式：

1. 專案推上 GitHub（`master` 或 `main`）
2. GitHub Repository Settings -> Pages -> Build and deployment 選擇 `GitHub Actions`
3. Workflow `Deploy gh-pages` 可手動觸發，或依排程（每月 5 日）自動執行

## Data Dictionary

請見：`www/DATA_DICTIONARY.md`
