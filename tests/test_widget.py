import pytest

from src.widget import format_transaction, get_date, mask_account_card


def test_mask_account_card_edge_cases():
    assert mask_account_card("") == "Номер не указан"
    assert mask_account_card("abc") == "Неверный формат номера"


def test_format_transaction_branches():
    tx = {
        "description": "Оплата",
        "operationAmount": {"amount": "0", "currency": {"code": "N/A"}},
    }
    out = format_transaction(tx)
    assert "Дата не указана" in out

    tx2 = {
        "date": "2024-01-01T00:00:00",
        "description": "Оплата",
        "operationAmount": {"amount": "10", "currency": {"code": "RUB"}},
        "to": "Счет 12345678901234567890",
    }
    out2 = format_transaction(tx2)
    assert "Получатель:" in out2 or "->" in out2


@pytest.mark.parametrize(
    "data, result",
    [
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305")
    ]
)
def test_get_mask_card_number(data, result):
    assert mask_account_card(data) == result


def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
