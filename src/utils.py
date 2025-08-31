import json
from pathlib import Path
from typing import List, Dict, Any


def load_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """
    Загружает финансовые транзакции из JSON-файла.

    Возвращает:
        List[Dict]: Список словарей с данными транзакций.
        Пустой список, если файл не найден, пуст, или данные некорректны.
    """
    path = Path(file_path)

    # Проверка существования файла
    if not path.is_file():
        return []

    try:
        # Чтение и парсинг файла
        with path.open(encoding='utf-8') as f:
            data = json.load(f)

            # Проверка типа данных
            if not isinstance(data, list):
                return []

            # Фильтрация только словарей
            return [item for item in data if isinstance(item, dict)]

    except (json.JSONDecodeError, UnicodeDecodeError, PermissionError):
        # Обработка ошибок чтения/парсинга
        return []
