from fastapi import FastAPI, Query
from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import sqlite3
import pandas as pd
import os
import psycopg2

app = FastAPI(title="Formation Internal Data Server")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# ---------------------------
# Trang chủ
# ---------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ---------------------------
# Hàm query chung
# ---------------------------
def query_db(sql, params=()):
    conn = psycopg2.connect(DATABASE_URL)
    df = pd.read_sql(sql, conn, params=params)
    conn.close()
    return df

# ---------------------------
# API lookup barcode
# ---------------------------
@app.get("/lookup/barcode")
def lookup_barcode(
    barcode: str = Query(..., description="Barcode Number"),
    limit: int = 100
):
    sql = f"""
        SELECT *
        FROM all_data
        WHERE "Barcode Number" = %s
        LIMIT 100
    """
    df = query_db(sql, (barcode,))
    return df.to_dict(orient="records")

# ---------------------------
# API lookup process
# ---------------------------
@app.get("/lookup/process")
def lookup_process(
    process: str = Query(..., description="Process name"),
    limit: int = 100
):
    sql = f"""
        SELECT *
        FROM all_data
        WHERE "Process name" = %s
        LIMIT 100
    """
    df = query_db(sql, (process,))
    return df.to_dict(orient="records")

# ---------------------------
# API lookup barcode + process
# ---------------------------
@app.get("/lookup")
def lookup(
    barcode: str | None = None,
    process: str | None = None,
    limit: int = 100
):
    where = []
    params = []

    if barcode:
        where.append("[Barcode Number] = ?")
        params.append(barcode)

    if process:
        where.append("[Process name] = ?")
        params.append(process)

    where_sql = " AND ".join(where) if where else "1=1"

    sql = f"""
        SELECT *
        FROM all_data
        WHERE {where_sql}
        LIMIT {limit}
    """

    df = query_db(sql, params)
    return df.to_dict(orient="records")


