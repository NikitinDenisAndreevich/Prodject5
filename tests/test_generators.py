import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions():
    return [
        {
            "description": "Organization Transfer",
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            }
        },
        {
            "description": "Transfer from account to account",
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            }
        },
        {
            "description": "Transfer from account to account",
            "operationAmount": {
                "currency": {
                    "code": "EUR"
                }
            }
        },
        {
            "description": "Transfer from card to card",
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            }
        }
    ]


def test_filter_by_currency(sample_transactions):
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    # Проверяем количество транзакций в USD
    assert len(usd_transactions) == 3
    # Проверяем описания
    assert usd_transactions[0]['description'] == "Organization Transfer"
    assert usd_transactions[1]['description'] == "Transfer from account to account"
    assert usd_transactions[2]['description'] == "Transfer from card to card"
    # Проверяем пустой список
    empty_transactions = list(filter_by_currency([], "USD"))
    assert len(empty_transactions) == 0


def test_transaction_descriptions(sample_transactions):
    descriptions = list(transaction_descriptions(sample_transactions))
    expected_descriptions = [
        "Organization Transfer",
        "Transfer from account to account",
        "Transfer from account to account",
        "Transfer from card to card"
    ]
    assert descriptions == expected_descriptions
    # Проверяем пустой список
    empty_descriptions = list(transaction_descriptions([]))
    assert len(empty_descriptions) == 0


@pytest.mark.parametrize("start, end, expected_numbers", [
    # Тест 1: генерация 1-5 с длиной 4 символа
    (1, 5, ["0000000000000001", "0000000000000002", "0000000000000003", "0000000000000004", "0000000000000005"]),

    # Тест 2: генерация 995-1000 (переход через разряд)
    (995, 1000, ["0000000000000995", "0000000000000996", "0000000000000997", "0000000000000998",
                 "0000000000000999", "0000000000001000"]),

    # Тест 3: граничные значения (0-1)
    (0, 1, ["0000000000000000", "0000000000000001"]),

    # Тест 4: одинаковые begin и end
    (1234, 1234, ["0000000000001234"])
])
def test_card_number_generator(start, end, expected_numbers):
    generated_numbers = list(card_number_generator(start, end))
    assert generated_numbers == expected_numbers, f"Ожидалось {expected_numbers}, получено {generated_numbers}"


# Тест на ошибки валидации
def test_card_number_generator_errors():
    with pytest.raises(ValueError):
        list(card_number_generator(-5, 10))  # Отрицательный begin

    with pytest.raises(ValueError):
        list(card_number_generator(10, 5))  # begin > end
