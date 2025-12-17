import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

DB_URL = "postgresql://neondb_owner:npg_5AZ9EfMmurpN@ep-spring-wind-a1olms9s-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine = create_engine(DB_URL)

folder = Path("Formation data server")

for file in folder.glob("data_cloud.db"):
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
