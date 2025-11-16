import sqlite3, json

DB_PATH = "/opt/ndloadouts/builds_bf.db"
OUT = "/var/www/html/export-bf-builds.json"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT * FROM bf_builds")
rows = c.fetchall()

export = []

for r in rows:
    export.append({
        "id": r["id"],
        "title": r["title"],
        "weapon_type": r["weapon_type"],
        "top": [r["top1"], r["top2"], r["top3"]],
        "date": r["date"],
        "mode": r["mode"],
        "categories": json.loads(r["categories"]) if r["categories"] else [],
        "tabs": json.loads(r["tabs"]) if r["tabs"] else [],
    })

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(export, f, ensure_ascii=False, indent=2)

print("ГОТОВО:", OUT)
