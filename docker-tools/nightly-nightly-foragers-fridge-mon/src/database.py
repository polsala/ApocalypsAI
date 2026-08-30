import sqlite3
from datetime import datetime, timedelta

DATABASE_FILE = 'fridge_monitor.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            added_date TEXT NOT NULL,
            spoil_days INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'fresh' -- 'fresh', 'consumed', 'spoiled'
        )
    ''')
    conn.commit()
    conn.close()

def add_item(name, spoil_days):
    conn = get_db_connection()
    cursor = conn.cursor()
    added_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO items (name, added_date, spoil_days) VALUES (?, ?, ?)',
                   (name, added_date, spoil_days))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id

def get_all_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE status = "fresh" ORDER BY added_date DESC')
    items = cursor.fetchall()
    conn.close()
    return [dict(item) for item in items]

def update_item_status(item_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET status = ? WHERE id = ?', (status, item_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print(f"Database '{DATABASE_FILE}' initialized.")
