from db.connection import get_conn

with get_conn() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database();")
        print(cur.fetchone())

# run it by cd .. and python -m scripts.test_db so it is a module        