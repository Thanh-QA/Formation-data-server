from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import pandas as pd
import psycopg2

# ===========================
# App init
# ===========================
app = FastAPI(title="Formation Internal Data Server")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

print("=== API VERSION: POSTGRES READY ===")

# ===========================
# Home page
# ===========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ===========================
# DB helper
# ===========================
def query_db(sql: str, params: tuple = ()):
    conn = psycopg2.connect(DATABASE_URL)
    try:
        df = pd.read_sql(sql, conn, params=params)
        return df
    finally:
        conn.close()

# ===========================
# Lookup barcode + process
# ===========================
@app.get("/lookup")
def lookup(
    batch: str | None = None,
    process: str | None = None,
    limit: int = %s
):
    where_clauses = []
    params = []

    # Tên cột trong DB: "batch" và "process_name"
    if batch:
        where_clauses.append("batch = %s")
        params.append(barcode)

    if process:
        where_clauses.append("process_name = %s")
        params.append(process)

    where_sql = " AND ".join(where_clauses) if where_clauses else "TRUE"

    sql = f"""
        SELECT *
        FROM public.all_data
        WHERE {where_sql}
        LIMIT %s
    """
    params.append(limit)
    print("SQL:", sql)
    print("PARAMS:", params)


    df = query_db(sql, tuple(params))
    return df.to_dict(orient="records")

