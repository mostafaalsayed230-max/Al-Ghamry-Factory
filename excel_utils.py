import pandas as pd
from database import get_connection

def export_raw_materials(file_path):
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM raw_materials", conn)
    df.to_excel(file_path, index=False)
    conn.close()

def import_raw_materials(file_path):
    df = pd.read_excel(file_path)
    conn = get_connection()
    c = conn.cursor()
    for _, row in df.iterrows():
        c.execute("""
            INSERT OR IGNORE INTO raw_materials (id, name, unit, current_stock, cost_per_unit)
            VALUES (?, ?, ?, ?, ?)
        """, (row['id'], row['name'], row['unit'], row['current_stock'], row['cost_per_unit']))
    conn.commit()
    conn.close()
