
from typing import Iterator


def filter_by_currency(transactions: list, currency: str) -> Iterator[dict]:

    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list) -> Iterator[str]:
    """Функция принимает список словарей с транзакциями
     и возвращает описание каждой операции по очереди."""

    for transaction in transactions:
        yield transaction.get("description")


def card_number_generator(begin: int, end: int) -> Iterator[str]:
    """Генерирует номера карт в диапазоне [begin, end] с ведущими нулями."""
    if begin < 0 or end < 0:
        raise ValueError("Диапазон не может быть отрицательным")
    if begin > end:
        raise ValueError("begin должен быть меньше или равен end")

    max_length = len(str(end))  # Определяем длину самого длинного номера

    for number in range(begin, end + 1):
        # Форматируем число, добавляя ведущие нули до max_length
        formatted_number = f"{number:0{max_length}d}"
        yield formatted_number