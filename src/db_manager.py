# src/db_manager.py
import os
import psycopg2
from psycopg2.extras import execute_values

class DBManager:
    def __init__(self):
        # We read these from the environment variables set by Docker Compose
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "visual_search"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "secretpassword"),
            host=os.getenv("DB_HOST", "localhost"), 
            port=os.getenv("DB_PORT", "5433")
        )
        # Enable auto-commit for simpler handling
        self.conn.autocommit = True

    def insert_batch(self, data_list):
        """
        data_list: list of tuples (filename, category, embedding_list)
        Efficiently inserts multiple rows at once.
        """
        cursor = self.conn.cursor()
        query = """
            INSERT INTO inventory (filename, category, embedding)
            VALUES %s
        """
        
        execute_values(cursor, query, data_list)
        cursor.close()
        print(f"Inserted {len(data_list)} records.")

    def search_similar(self, query_vector, limit=5):
        """
        Returns the top 'limit' closest images.
        """
        cursor = self.conn.cursor()
        sql = """
            SELECT filename, category, (embedding <=> %s::vector) as distance
            FROM inventory
            ORDER BY distance ASC
            LIMIT %s;
        """
        # pgvector expects the vector as a standard list/array
        cursor.execute(sql, (query_vector, limit))
        results = cursor.fetchall()
        cursor.close()
        return results

    def close(self):
        self.conn.close()