# TWFS Jupyter EDA

## 1) 安裝（建議使用虛擬環境）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-notebook.txt
```

## 2) 建立資料庫

```bash
python pipelines/build_databases.py --base-path .
```

## 3) 開啟 Notebook

```bash
jupyter lab output/jupyter-notebook/twfs-duckdb-eda.ipynb
```

Notebook 內容包含：
- DuckDB 連線與資料概況
- 指定銀行關鍵字搜尋
- 指定銀行逐月趨勢（含簡易圖）
