import json
from pathlib import Path
from typing import Any, Dict, List


def load_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """
    Загружает финансовые транзакции из JSON-файла с валидацией структуры.
    Обрабатывает основные файловые ошибки и ошибки формата данных.
    """
    path = Path(file_path)

    try:
        if not path.is_file():
            return []

        with path.open(encoding='utf-8') as f:
            data = json.load(f)

        return [
            item for item in data
            if isinstance(item, dict)
            and isinstance(item.get("operationAmount"), dict)
            and "amount" in item["operationAmount"]
            and "currency" in item["operationAmount"]
        ]

    except (FileNotFoundError, json.JSONDecodeError,
            UnicodeDecodeError, PermissionError):
        return []
