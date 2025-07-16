import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "onlinestore"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "admin123"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", 5432),
        cursor_factory=RealDictCursor  
    )
    return conn

