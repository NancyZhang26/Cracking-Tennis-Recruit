import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
load_dotenv()

def get_conn(): 
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("USER_NAME"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        row_factory=dict_row
    )

print(get_conn())
