# Data Dictionary

## Source Row Schema (`facts`)

| Field | Type | Description |
|---|---|---|
| `dataset` | TEXT | 資料集代碼（例如 `CC`, `LN`, `CL_INFO`） |
| `roc_ym` | TEXT | 民國年月（例如 `10001`） |
| `ad_year` | INTEGER | 西元年（`roc_ym` 年 + 1911） |
| `month` | INTEGER | 月份（1-12） |
| `month_key` | TEXT | 西元年月（`YYYY-MM`） |
| `institution` | TEXT | 機構名稱（來源欄位：`銀行`） |
| `institution_type` | TEXT | 機構類型（來源欄位：`銀行類別`） |
| `item_zh` | TEXT | 中文指標名稱（來源欄位：`項目`） |
| `item_en` | TEXT | 英文欄位代碼（來源欄位：`英文欄位` 或 `英文項目`） |
| `value_raw` | TEXT | 原始字串數值（來源欄位：`數值`） |
| `value_num` | REAL/DOUBLE | 轉換後可計算數值（失敗時為 `NULL`） |
| `source_file` | TEXT | 來源 CSV 檔案路徑 |

## Static Web Data

| File | Description |
|---|---|
| `www/data/catalog.json` | 目錄與索引（月份、機構、資料集、總筆數、生成時間） |
| `www/data/by_month/<YYYY-MM>.json` | 單月所有資料列 |
| `www/data/by_institution/<file>.json` | 單一機構跨月資料列 |

## Data Refresh

- Crawler: `pipelines/crawl_latest.py`
- DB + Web build: `pipelines/build_databases.py`
- DuckDB analysis helper: `pipelines/analyze_duckdb.py`
