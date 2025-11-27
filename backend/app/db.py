import sqlite3
from pathlib import Path

# Path to sqlite DB file (backend/data.db)
DB_PATH = Path(__file__).parent.parent / "data.db"

def init_db():
    """
    Initialize the sqlite database and create tables if they don't already exist.
    This runs at app startup for local development convenience.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )""")
    conn.commit()
    conn.close()

def get_conn():
    """
    Return a sqlite3 connection object.
    check_same_thread=False lets sqlite connections be used across threads
    which helps when using uvicorn reload/dev server.
    """
    return sqlite3.connect(DB_PATH, check_same_thread=False)
