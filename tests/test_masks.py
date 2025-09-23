import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("data, expected", [
    ("3421324443211452", "**1452"),
    ("34298761324443211452", "**1452"),
    ("3421324443211952", "**1952")
])
def test_get_mask_account(data, expected):
    """Проверка маскирования номера счёта"""
    assert get_mask_account(data) == expected


def test_get_mask_card_number():

    assert "2543 36** **** 1234" == get_mask_card_number("2543362543361234")


def test_get_mask_account_exception():
    # Передаем некорректный тип (int), чтобы внутри произошла ошибка индексации
    # и сработал блок except, возвращающий пустую строку
    assert get_mask_account(12345678901234567890) == ""
