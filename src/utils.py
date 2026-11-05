import json
from pathlib import Path

def zip_transactions_from_json(file_path: str | Path) -> list[dict]:
    path = Path(file_path)
    if not path.exists():
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []
