import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# SQLite file
sqlite_file = "data_cloud.db"
sqlite_conn = sqlite3.connect(sqlite_file)

# PostgreSQL
DB_URL = "postgresql://thanhformation:3Sp48UmuBx5FuJ9ELUENluGOc3lHssBx@dpg-d51edgggjchc73b4tes0-a/data_cloud"
pg_engine = create_engine(DB_URL)

# Lấy danh sách bảng trong SQLite
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", sqlite_conn)

for table in tables['name']:
    df = pd.read_sql(f"SELECT * FROM {table}", sqlite_conn)

    # Chuẩn hóa cột
    df.columns = df.columns.str.strip().str.lower()
    df.rename(columns={
        "cell barcode": "barcode",
        "process name": "process_name",
        "cellstate": "cell_state"
    }, inplace=True)

    # Loại bỏ space thừa
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.strip()

    # Ghi sang PostgreSQL
    df.to_sql("all_data", pg_engine, if_exists="replace", index=False)
