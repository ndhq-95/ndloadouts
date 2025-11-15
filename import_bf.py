from fastapi import APIRouter
import sqlite3
from pathlib import Path

router = APIRouter(prefix="/api/bf/modules")
DB_PATH = Path("/opt/ndloadouts/builds_bf.db")

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/all")
def get_all_modules():
    conn = connect()

    rows = conn.execute("""
        SELECT 
            m.id,
            m.weapon_type,
            m.category,
            m.en,
            m.pos,
            wt.label AS weapon_label
        FROM bf_modules AS m
        LEFT JOIN bf_weapon_types AS wt
            ON wt.key = m.weapon_type
        ORDER BY m.weapon_type, m.category, m.pos
    """).fetchall()

    result = {}

    for r in rows:
        w_type = r["weapon_type"]

        if w_type not in result:
            result[w_type] = {
                "weapon_label": r["weapon_label"],
                "modules": {}
            }

        if r["category"] not in result[w_type]["modules"]:
            result[w_type]["modules"][r["category"]] = []

        result[w_type]["modules"][r["category"]].append({
            "id": r["id"],
            "name_en": r["en"],
            "pos": r["pos"]
        })

    return result
