import sqlite3
from datetime import datetime

DB_NAME = "database.db"

def get_connection():
    conn = sqlite3.connect(
        DB_NAME,
        timeout=15,
        check_same_thread=False
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT UNIQUE,
            product_name TEXT,
            block_hash TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            status TEXT,
            verified_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_product(product_id, product_name, block_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (product_id, product_name, block_hash, created_at)
        VALUES (?, ?, ?, ?)
    """, (product_id, product_name, block_hash, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, product_name, block_hash
        FROM products WHERE product_id = ?
    """, (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def log_verification(product_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO verification_logs (product_id, status, verified_at)
        VALUES (?, ?, ?)
    """, (product_id, status, datetime.now().isoformat()))
    conn.commit()
    conn.close()
