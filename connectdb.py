import psycopg2

conn = psycopg2.connect(
    "postgresql://thanhformation:3Sp48UmuBx5FuJ9ELUENluGOc3lHssBx@dpg-d51edgggjchc73b4tes0-a/data_cloud"
)
print("CONNECTED")
conn.close()

