# app/database/db_handler.py
import sqlite3
from datetime import datetime

DB_PATH = "rag_metadata.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        chunk_count INTEGER,
        upload_time TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_metadata(filename, chunk_count):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (filename, chunk_count, upload_time) VALUES (?, ?, ?)",
        (filename, chunk_count, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_all_metadata():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "filename": r[1], "chunks": r[2], "upload_time": r[3]} for r in rows]
