import os
import requests
from typing import Dict, Optional

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"

def get_exchange_rate(base_currency: str) -> Optional[float]:
    """Получает текущий курс валюты к RUB через API"""
    if not API_KEY:
        raise ValueError("API key not configured")

    try:
        response = requests.get(
            BASE_URL,
            params={'base': base_currency, 'symbols': 'RUB'},
            headers={'apikey': API_KEY},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data['rates']['RUB']
    except (requests.RequestException, KeyError, ValueError):
        return None

def convert_amount_to_rub(transaction: Dict) -> Optional[float]:
    """Конвертирует сумму транзакции в рубли"""
    try:
        amount = float(transaction['operationAmount']['amount'])
        currency = transaction['operationAmount']['currency']['code']
    except (KeyError, ValueError, TypeError):
        return None

    if currency == 'RUB':
        return amount

    if currency not in {'USD', 'EUR'}:
        return None

    rate = get_exchange_rate(currency)
    return round(amount * rate, 2) if rate else None
