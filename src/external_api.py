import json
import os
from typing import Dict, Optional

import requests

API_KEY = os.getenv('API_KEY')
CONVERT_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_exchange_rate(base_currency: str) -> Optional[float]:
    """Получает текущий курс валюты к RUB через API"""
    if not API_KEY:
        raise ValueError("API key not configured")

    try:
        response = requests.get(
            CONVERT_URL,
            params={
                'amount': 1,
                'from': base_currency,
                'to': 'RUB'
            },
            headers={'apikey': API_KEY},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return float(data['result'])
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Ошибка получения курса: {e}")
        return None


def convert_amount_to_rub(transaction: Dict) -> Optional[float]:
    """Конвертирует сумму транзакции в рубли"""
    try:
        amount = float(transaction['operationAmount']['amount'])
        currency = transaction['operationAmount']['currency']['code']
    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка извлечения данных: {e}")
        return None

    if currency == 'RUB':
        return amount

    if currency not in {'USD', 'EUR'}:
        return None

    rate = get_exchange_rate(currency)
    return round(amount * rate, 2) if rate else None


def open_json_file(file_path: str) -> Optional[dict]:
    """Чтение JSON-файла с обработкой ошибок"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден!")
        return None
    except json.JSONDecodeError:
        print("Ошибка формата JSON!")
        return None
