# db.py
import psycopg2
from pgvector.psycopg2 import register_vector

from .config import DB_DSN

def get_conn():
    conn = psycopg2.connect(DB_DSN)
    register_vector(conn)
    return conn
