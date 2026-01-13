import sqlite3
from datetime import datetime
import hashlib

DB_FILE = "factory.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # مستخدمين
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        role TEXT,
        created_at TEXT
    )
    """)

    # المواد الخام
    c.execute("""
    CREATE TABLE IF NOT EXISTS raw_materials (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        unit TEXT,
        current_stock REAL DEFAULT 0,
        cost_per_unit REAL
    )
    """)

    # المنتجات
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        selling_price REAL
    )
    """)

    # وصفة الإنتاج
    c.execute("""
    CREATE TABLE IF NOT EXISTS production_recipes (
        product_id INTEGER,
        raw_material_id INTEGER,
        quantity_needed REAL,
        PRIMARY KEY(product_id, raw_material_id)
    )
    """)

    # سجل الإنتاج
    c.execute("""
    CREATE TABLE IF NOT EXISTS production_logs (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity_produced INTEGER,
        date TEXT
    )
    """)

    # الفواتير
    c.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY,
        customer_name TEXT,
        total_amount REAL,
        paid_amount REAL DEFAULT 0,
        date TEXT
    )
    """)

    # تفاصيل الفواتير
    c.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items (
        invoice_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price_per_unit REAL
    )
    """)

    # المصروفات
    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        description TEXT,
        amount REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

# ===== المستخدمين =====
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def admin_exists():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE role='admin'")
    exists = c.fetchone()
    conn.close()
    return bool(exists)

def create_admin(username, password):
    conn = get_connection()
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, 'admin', ?)",
              (username, hashed, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("SELECT role FROM users WHERE username=? AND password_hash=?", (username, hashed))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
