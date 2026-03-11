import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

db = BASE_DIR / "db.sqlite3"
schema = BASE_DIR / "sql/schema.sql"
seed = BASE_DIR / "sql/seed.sql"

conn = sqlite3.connect(db)

with open(schema) as f:
    conn.executescript(f.read())

with open(seed) as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database initialized")