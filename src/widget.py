from src import masks
from datetime import datetime
from typing import Dict, Optional


def mask_account_card(number: str) -> str:
    """Маскирует номер карты или счета с автоматическим определением типа"""
    if not number:
        return "Номер не указан"

    normalized = number.lower().replace(" ", "")
    is_account = "счет" in normalized
    digits = "".join(c for c in normalized if c.isdigit())

    try:
        if is_account or len(digits) == 20:  # Счет
            return masks.mask_account(digits)
        elif 16 <= len(digits) <= 20:  # Карта
            return masks.mask_card_number(digits)
        else:
            return "Неверный формат номера"
    except (ValueError, IndexError):
        return "Ошибка маскирования"


def get_date(date_str: str) -> Optional[str]:
    """Преобразует дату из ISO формата в DD.MM.YYYY с обработкой ошибок"""
    if not date_str:
        return None

    try:
        dt = datetime.fromisoformat(date_str.replace('Z', ''))  # Для Python 3.11+
        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return None


def format_transaction(tx: Dict) -> str:
    """Форматирует транзакцию для вывода с защитой от отсутствующих данных"""
    parts = []

    # Дата
    raw_date = tx.get('date')
    formatted_date = get_date(raw_date) if raw_date else "Дата не указана"
    description = tx.get('description', 'Без описания')
    parts.append(f"{formatted_date} {description}")

    # Отправитель/получатель
    from_account = mask_account_card(tx.get('from', ''))
    to_account = mask_account_card(tx.get('to', ''))

    if from_account and to_account:
        parts.append(f"{from_account} -> {to_account}")
    elif to_account:
        parts.append(f"Получатель: {to_account}")
    elif from_account:
        parts.append(f"Отправитель: {from_account}")

    # Сумма и валюта
    amount = tx.get('amount', 0)
    currency = tx.get('currency', 'N/A')
    parts.append(f"Сумма: {amount} {currency}")

    return '\n'.join(parts)
