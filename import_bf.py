import json
import sqlite3
from pathlib import Path

# Пути
DATA_FILE = Path("/opt/ndloadouts/data/modules-shv.json")
DB_PATH = Path("/opt/ndloadouts/builds_bf.db")
EXPORT_PATH = Path("/opt/bf_modules_full.json")

output = {}

# --- 1. Добавляем JSON-модули (shared) ---

if DATA_FILE.exists():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        output["shv"] = json.load(f)
else:
    output["shv"] = {}

# --- 2. Подтягиваем модули из SQLite ---

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

rows = conn.execute("""
    SELECT weapon_type, category, en, pos 
    FROM bf_modules
    ORDER BY weapon_type, category, pos
""").fetchall()

conn.close()

for r in rows:
    w = r["weapon_type"]
    c = r["category"]
    name = r["en"]

    if w not in output:
        output[w] = {}

    if c not in output[w]:
        output[w][c] = []

    # Добавляем только если ещё нет
    if name not in output[w][c]:
        output[w][c].append(name)

# --- 3. Сохраняем ---

with open(EXPORT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("BF FULL EXPORT →", EXPORT_PATH)



@app.get("/api/bf/export/full")
def bf_export_full():
    return FileResponse(
        "/opt/bf_modules_full.json",
        filename="bf_modules_full.json",
        media_type="application/json"
    )
