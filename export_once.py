import sqlite3
import re

DB = "/opt/NDHQ-Ecosystem/apps/backend/bf_builds.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

bad = cur.execute("SELECT id, tabs_json FROM builds WHERE json_valid(tabs_json)=0").fetchall()

print("Найдено битых:", len(bad))

# паттерн для 20" FACTORY → 20 FACTORY
pattern = re.compile(r'(\d+(\.\d+)?)" ?([A-Za-zА-Яа-я0-9\-\.\s]+)"')

for row in bad:
    id = row["id"]
    raw = row["tabs_json"]

    # заменяем такие строки на без кавычек
    fixed = pattern.sub(r'\1 \3', raw)

    # ещё удаляем одиночные кавычки внутри слов
    fixed = fixed.replace('\\"', '')

    # пробуем проверить валидность
    ok = cur.execute("SELECT json_valid(?)", (fixed,)).fetchone()[0]

    if ok:
        print(f"[OK] FIXED id={id}")
        cur.execute("UPDATE builds SET tabs_json=? WHERE id=?", (fixed, id))
        conn.commit()
    else:
        print(f"[FAIL] id={id} всё ещё битое")
        print("RAW:", raw)
        print("NEW:", fixed)

print("=== DONE ===")
