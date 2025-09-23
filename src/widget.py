from datetime import datetime
from typing import Dict, Optional

from src import masks


def mask_account_card(number: str) -> str:
    """Маскирует номер карты или счета с автоматическим определением типа"""
    if not number:
        return "Номер не указан"

    # Сохраняем префикс (например, "Счет", "Visa Classic" и т.п.)
    parts = number.split()
    prefix = ""
    if parts:
        # Префикс — все, кроме последнего токена, если последний — цифры
        if any(ch.isdigit() for ch in parts[-1]):
            prefix = " ".join(parts[:-1]).strip()
        else:
            prefix = " ".join(parts).strip()

    normalized = number.lower().replace(" ", "")
    is_account = "счет" in normalized
    digits = "".join(c for c in number if c.isdigit())

    try:
        if is_account or len(digits) == 20:  # Счет
            masked = masks.get_mask_account(digits)
            return f"{prefix} {masked}".strip() if prefix else masked
        elif 16 <= len(digits) <= 20:  # Карта
            masked = masks.get_mask_card_number(digits)
            return f"{prefix} {masked}".strip() if prefix else masked
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

    # Сумма и валюта (operationAmount)
    op = tx.get('operationAmount') or {}
    amount = op.get('amount', 0)
    curr = op.get('currency') or {}
    currency_code = curr.get('code', 'N/A')
    parts.append(f"Сумма: {amount} {currency_code}")

    return '\n'.join(parts)
