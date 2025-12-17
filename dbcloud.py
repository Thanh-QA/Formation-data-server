import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

DATABASE_URL = "postgresql://thanhformation:3Sp48UmuBx5FuJ9ELUENluGOc3lHssBx@dpg-d51edgggjchc73b4tes0-a/data_cloud"
engine = create_engine(DATABASE_URL)

folder = Path("Formation data server")

for file in folder.glob("DATABASE_URL"):
    xls = pd.ExcelFile(file)
    for sheet in xls.sheet_names:
        print(f"Import {file.name} | {sheet}")

        df = pd.read_excel(file, sheet_name=sheet, dtype=str)

        df.columns = df.columns.str.strip().str.lower()

        df = df.rename(columns={
            "cell barcode": "barcode",
            "cellstate": "cell_state",
            "process name": "process_name"
        })

        df["source_file"] = file.name
        df["source_sheet"] = sheet

        df.to_sql(
            "all_data",
            engine,
            if_exists="append",
            index=False,
            chunksize=10000
        )

print("IMPORT DONE")
