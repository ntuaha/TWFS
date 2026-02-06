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
- `/docs/ISSUE_RESOLUTION.md`：歷史 open issues 對應解法

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
python pipelines/crawl_latest.py --base-path . --source openapi
python pipelines/build_databases.py --base-path .
```

新資料來源（預設）：`https://stat.fsc.gov.tw/FSC_OAS3_RESTORE/api/CSV_EXPORT`  
舊來源相容模式：`python pipelines/crawl_latest.py --base-path . --source legacy`

說明：
- 網頁可用「銀行搜尋」直接篩選指定銀行資訊（避免機構清單過長）
- 爬蟲會自動從新站頁面偵測可用 `TableID`（`Bxx`），降低手動維護成本

## GitHub Actions / gh-pages

已提供 workflow：

- `/.github/workflows/ci.yml`
- `/.github/workflows/monthly-update.yml`（每月自動爬蟲、重建、提交更新）
- `/.github/workflows/deploy-gh-pages.yml`

啟用方式：

1. 專案推上 GitHub（`master` 或 `main`）
2. GitHub Repository Settings -> Pages -> Build and deployment 選擇 `GitHub Actions`
3. Workflow `Monthly Data Update` 每月 1 日 UTC 03:10 自動執行資料更新並提交
4. `master/main` 有新 commit 後，`Deploy gh-pages` 會自動部署網站

## Data Dictionary

請見：`www/DATA_DICTIONARY.md`
