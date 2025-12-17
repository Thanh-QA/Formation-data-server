from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

engine = create_engine(
    "postgresql://neondb_owner:npg_5AZ9EfMmurpN@ep-spring-wind-a1olms9s-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    pool_size=10,
    max_overflow=20
)

@app.get("/lookup")
def lookup(process: str, limit: int = 5000):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT barcode, cell_state, process_name, ocv, ir, k1
                FROM all_data
                WHERE process_name = :process
                LIMIT :limit
            """),
            {"process": process, "limit": limit}
        )
        return [dict(r._mapping) for r in result]
