from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
import sqlite3, json
from pathlib import Path

router = APIRouter(prefix="/api/bf", tags=["BF Import/Export"])

DB_PATH = Path("/opt/ndloadouts/builds_bf.db")
EXPORT_PATH = Path("/opt/bf_modules_export.json")


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/import-modules")
def import_and_get_link():
    conn = connect()

    rows = conn.execute("""
        SELECT id, weapon_type, category, en, pos
        FROM bf_modules
        ORDER BY weapon_type, category, pos
    """).fetchall()

    # Сохранение в файл
    with open(EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump([dict(r) for r in rows], f, ensure_ascii=False, indent=2)

    # Возвращаем ссылку для скачивания
    return {
        "status": "ok",
        "download_url": "/api/bf/download-modules"
    }


@router.get("/download-modules")
def download_bf_modules():
    if not EXPORT_PATH.exists():
        return JSONResponse({"error": "Файл не найден"}, status_code=404)

    return FileResponse(
        EXPORT_PATH,
        filename="bf_modules_export.json",
        media_type="application/json"
    )
