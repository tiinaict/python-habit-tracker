# storage.py
# Yksinkertainen JSON-tallennus

import json
from pathlib import Path

DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "habits.json"

def load_data() -> list:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        save_data([])  # luo tyhjä tietokanta
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data: list) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)