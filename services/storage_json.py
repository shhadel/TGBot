import json
from pathlib import Path
from typing import Dict

DATA_FILE = Path("birthdays.json")

def load_birthdays() -> Dict[int, Dict[str, str]]:
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}

def save_birthdays(data: Dict[int, Dict[str, str]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in data.items()}, f, indent=2)