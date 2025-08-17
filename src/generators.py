from typing import Iterator


def filter_by_currency(transactions: list, currency: str) -> Iterator[dict]:
    """
    Фильтрует транзакции по коду валюты.

    Args:
        transactions: Список транзакций (словари с ключом 'operationAmount' -> 'currency' -> 'code').
        currency: Трёхбуквенный код валюты (например, 'USD', 'RUB').

    Yields:
        Транзакции, у которых код валюты совпадает с заданным.

    Примечание:
        Проверка регистрозависима. Транзакции с некорректной структурой игнорируются.
    """
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list) -> Iterator[str]:
    """
    Возвращает итератор с описаниями транзакций.

    Args:
        transactions: Список транзакций (словари с ключом 'description').

    Yields:
        Описание транзакции. Транзакции без ключа 'description' пропускаются.
    """
    for transaction in transactions:
        yield transaction.get("description")


def card_number_generator(begin: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт в формате 16 цифр с ведущими нулями.

    Args:
        begin: Начальный номер (включительно).
        end: Конечный номер (включительно).

    Yields:
        Номер карты в формате '0000000000000001'.

    Raises:
        ValueError: При некорректном диапазоне (begin > end или отрицательные значения).

    Примечание:
        Максимальное поддерживаемое значение: 9999999999999999.
    """
    if begin < 0 or end < 0:
        raise ValueError("Диапазон не может быть отрицательным")
    if begin > end:
        raise ValueError("begin должен быть меньше или равен end")

    card_length = 16
    for number in range(begin, end + 1):
        formatted_number = f"{number:0{card_length}d}"
        yield formatted_number