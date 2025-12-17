import psycopg2

conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_5AZ9EfMmurpN@ep-spring-wind-a1olms9s-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)
print("CONNECTED")
conn.close()
