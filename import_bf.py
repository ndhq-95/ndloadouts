from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(prefix="/api/bf/export", tags=["BF Export"])

EXPORT_PATH = Path("/opt/bf_modules_export.json")

@router.get("/modules")
def download_bf_modules():
    if not EXPORT_PATH.exists():
        return {"error": "Файл не найден"}
    return FileResponse(
        EXPORT_PATH,
        filename="bf_modules_export.json",
        media_type="application/json"
    )
