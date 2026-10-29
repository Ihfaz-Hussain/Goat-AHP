import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

schema_path = (
    ROOT / "data" / "database" / "football_schema.sql"
)

database_path = (
    ROOT / "data" / "database" / "football.db"
)

with sqlite3.connect(database_path) as conn:
    conn.execute("PRAGMA foreign_keys = ON")

    with open(schema_path, encoding="utf-8") as f:
        conn.executescript(f.read())

print("Football database created successfully!")
