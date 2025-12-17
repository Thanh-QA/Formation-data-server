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
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

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
# Lookup by barcode
# ===========================
@app.get("/lookup/barcode")
def lookup_barcode(
    barcode: str = Query(..., description="Barcode Number"),
    limit: int = 100
):
    sql = """
        SELECT *
        FROM all_data
        WHERE "Barcode Number" = %s
        LIMIT %s
    """
    df = query_db(sql, (barcode, limit))
    return df.to_dict(orient="records")

# ===========================
# Lookup by process
# ===========================
@app.get("/lookup/process")
def lookup_process(
    process: str = Query(..., description="Process name"),
    limit: int = 100
):
    sql = """
        SELECT *
        FROM all_data
        WHERE "Process name" = %s
        LIMIT %s
    """
    df = query_db(sql, (process, limit))
    return df.to_dict(orient="records")

# ===========================
# Lookup barcode + process
# ===========================
@app.get("/lookup")
def lookup(
    barcode: str | None = None,
    process: str | None = None,
    limit: int = 100
):
    where_clauses = []
    params = []

    if barcode:
        where_clauses.append('"Barcode Number" = %s')
        params.append(barcode)

    if process:
        where_clauses.append('"Process name" = %s')
        params.append(process)

    where_sql = " AND ".join(where_clauses) if where_clauses else "TRUE"

    sql = f"""
        SELECT *
        FROM all_data
        WHERE {where_sql}
        LIMIT %s
    """
    params.append(limit)

    df = query_db(sql, tuple(params))
    return df.to_dict(orient="records")
