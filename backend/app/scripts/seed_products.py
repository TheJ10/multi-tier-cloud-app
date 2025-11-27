#!/usr/bin/env python3
"""
Seed the local sqlite database with sample products.

This script is safe to run multiple times: it will insert sample rows every run.
It writes to backend/data.db (same DB used by the app).
Run with:
    python backend/app/scripts/seed_products.py
or
    python -c "from backend.app.scripts.seed_products import seed; seed()"
"""
from pathlib import Path
import sqlite3

DB = Path(__file__).resolve().parents[2] / "data.db"

SAMPLES = [
    ("T-Shirt", 499.0, 20, "Comfortable cotton t-shirt"),
    ("Sneakers", 2499.0, 10, "Running shoes"),
    ("Backpack", 1299.0, 15, "Durable backpack"),
    ("Headphones", 1999.0, 5, "Noise-cancelling headphones"),
    ("Water Bottle", 199.0, 30, "Insulated stainless steel bottle")
]

def seed():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    # Ensure tables exist (same DDL as db.init_db)
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
    # Insert samples
    cur.executemany(
        "INSERT INTO products (name, price, stock, description) VALUES (?, ?, ?, ?)",
        SAMPLES
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(SAMPLES)} sample products into {DB}")

if __name__ == "__main__":
    seed()
