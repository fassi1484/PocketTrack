import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "expenses.db"

connection = sqlite3.connect(DB_PATH)

connection.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        notes TEXT DEFAULT ''
    )
""")

connection.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        month TEXT PRIMARY KEY,
        amount REAL NOT NULL
    )
""")

connection.commit()
connection.close()

print("PocketTrack database tables initialized successfully!")
