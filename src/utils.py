import json
from pathlib import Path
from typing import List, Dict, Any


def load_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """
    Загружает финансовые транзакции из JSON-файла с валидацией структуры.
    """
    path = Path(file_path)

    if not path.is_file():
        return []

    try:
        with path.open(encoding='utf-8') as f:
            data = json.load(f)

        return [
            item for item in data
            if isinstance(item, dict)
            and item.get("operationAmount")
            and isinstance(item["operationAmount"], dict)
            and "amount" in item["operationAmount"]
            and "currency" in item["operationAmount"]
        ]

    except (json.JSONDecodeError, UnicodeDecodeError, PermissionError):
        return []
