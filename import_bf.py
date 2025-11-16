from fastapi import FastAPI
from fastapi.responses import FileResponse
import sqlite3, json, os

app = FastAPI()

DB_PATH = "/opt/ndloadouts/builds_bf.db"
EXPORT_PATH = "/opt/ndloadouts/bf_builds_export.json"

@app.get("/export-bf-builds")
def export_bf_builds():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM bf_builds")
    rows = c.fetchall()

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

    with open(EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)

    return FileResponse(
        EXPORT_PATH,
        filename="bf_builds_export.json",
        media_type="application/json"
    )
