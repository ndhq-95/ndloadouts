import sqlite3
import json

DB_PATH = "/opt/ndloadouts/builds_bf.db"
OUTPUT = "bf_builds_export.json"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM bf_builds")
rows = cursor.fetchall()

export = []

for r in rows:
    item = {
        "id": r["id"],
        "title": r["title"],
        "weapon_type": r["weapon_type"],
        "top": [r["top1"], r["top2"], r["top3"]],
        "date": r["date"],
        "mode": r["mode"],
        "categories": json.loads(r["categories"]) if r["categories"] else [],
        "tabs": json.loads(r["tabs"]) if r["tabs"] else [],
    }
    export.append(item)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(export, f, ensure_ascii=False, indent=2)

print(f"Экспортировано {len(export)} сборок → {OUTPUT}")
