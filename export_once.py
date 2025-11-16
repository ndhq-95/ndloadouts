import sqlite3
import re
import json

DB = "/opt/NDHQ-Ecosystem/apps/backend/bf_builds.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

bad = cur.execute("SELECT id, tabs_json FROM builds").fetchall()

# паттерн:  20" FACTORY  →  20 FACTORY
# паттерн:  16.5" FLUTED → 16.5 FLUTED
pattern = re.compile(r'(\d+(?:\.\d+)?)" ?([A-Za-zА-Яа-я0-9\-\.\s]+)')

for row in bad:
    id = row["id"]
    raw = row["tabs_json"]
    fixed = pattern.sub(r'\1 \2', raw)  # убираем кавычку между числом и словом

    # пробуем JSON
    try:
        json.loads(fixed)
        cur.execute("UPDATE builds SET tabs_json=? WHERE id=?", (fixed, id))
        conn.commit()
        print(f"[OK] id={id}")
    except Exception as e:
        print(f"[FAIL] id={id} — still bad")
        print("RAW:", raw)
        print("NEW:", fixed)

print("=== DONE ===")
