import sqlite3
from contextlib import contextmanager
from datetime import datetime
import os

DATABASE_PATH = "inventory.db"

def init_db():
    """Initialize SQLite database with schema."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # PRODUCT table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            ean TEXT PRIMARY KEY,
            style_name TEXT NOT NULL,
            size TEXT NOT NULL,
            brand TEXT NOT NULL,
            style_design_code TEXT,
            model_no TEXT
        )
    """)
    
    # STORE table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store (
            store_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT NOT NULL UNIQUE
        )
    """)
    
    # USER table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    
    # INVENTORY table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_ean TEXT NOT NULL,
            store_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (product_ean) REFERENCES product(ean),
            FOREIGN KEY (store_id) REFERENCES store(store_id),
            UNIQUE(product_ean, store_id)
        )
    """)
    
    # TRANSACTION table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaction (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_ean TEXT NOT NULL,
            store_id INTEGER NOT NULL,
            quantity_change INTEGER NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Import', 'Transfer', 'Sale')),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_ean) REFERENCES product(ean),
            FOREIGN KEY (store_id) REFERENCES store(store_id)
        )
    """)
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def seed_initial_data():
    """Seed initial stores and test data."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if stores already exist
        cursor.execute("SELECT COUNT(*) FROM store")
        if cursor.fetchone()[0] == 0:
            stores = [
                ("Store 1",),
                ("Store 2",),
                ("Store 3",),
                ("Store 4",),
            ]
            cursor.executemany("INSERT INTO store (store_name) VALUES (?)", stores)
            conn.commit()
