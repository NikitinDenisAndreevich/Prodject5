import json
from pathlib import Path
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)

    # Проверка существования файла
    if not path.is_file():
        return []

    try:
        # Чтение и обработка файла
        with path.open(encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
    except PermissionError:
        return []

    # Проверка типа данных
    if not isinstance(data, list):
        return []

    valid_transactions = []
    for item in data:
        # Базовые проверки структуры
        if not isinstance(item, dict):
            continue

        # Проверка обязательных полей
        required_fields = {'id', 'state', 'operationAmount'}
        if not required_fields.issubset(item.keys()):
            continue

        # Проверка operationAmount
        operation_amount = item.get('operationAmount')
        if not isinstance(operation_amount, dict):
            continue

        # Проверка валюты и суммы
        if not all(key in operation_amount for key in ('amount', 'currency')):
            continue

        currency = operation_amount.get('currency')
        if not isinstance(currency, dict) or not {'name', 'code'}.issubset(currency.keys()):
            continue

        # Фильтрация по статусу
        if item.get('state') != 'EXECUTED':
            continue

        valid_transactions.append(item)

    return valid_transactions
