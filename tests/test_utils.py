import json
from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_file_not_found():
    with patch("pathlib.Path.is_file") as mock_is_file:
        mock_is_file.return_value = False
        result = load_transactions("non_existent.json")
        assert result == []


def test_empty_file():
    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open", mock_open(read_data="")):
        mock_is_file.return_value = True
        result = load_transactions("empty.json")
        assert result == []


def test_invalid_json():
    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open", mock_open(read_data='{invalid json')):
        mock_is_file.return_value = True
        result = load_transactions("invalid.json")
        assert result == []


def test_not_a_list():
    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open", mock_open(read_data='{"key": "value"}')):
        mock_is_file.return_value = True
        result = load_transactions("not_a_list.json")
        assert result == []


def test_mixed_data_types_in_list():
    test_data = [
        # Валидный элемент
        {
            "id": 1,
            "operationAmount": {
                "amount": 100,
                "currency": {"name": "USD", "code": "USD"}
            }
        },
        # Невалидные элементы
        "invalid_item",
        123,
        # Валидный элемент
        {
            "id": 2,
            "operationAmount": {
                "amount": 200,
                "currency": {"name": "EUR", "code": "EUR"}
            }
        }
    ]

    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open", mock_open(read_data=json.dumps(test_data))):
        mock_is_file.return_value = True
        result = load_transactions("mixed_data.json")
        assert len(result) == 2, "Должны остаться только 2 валидных транзакции"
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open", mock_open(read_data=json.dumps(test_data))):
        mock_is_file.return_value = True
        result = load_transactions("mixed_data.json")
        assert len(result) == 2
        assert all(isinstance(item, dict) for item in result)


def test_valid_transactions():
    test_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"}
            }
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "USD", "code": "USD"}
            }
        }
    ]

    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open", mock_open(read_data=json.dumps(test_data))):
        mock_is_file.return_value = True
        result = load_transactions("valid_data.json")
        assert len(result) == 2
        assert all(key in item for item in result for key in ["id", "state", "operationAmount"])
        assert result[0]["operationAmount"]["amount"] == "31957.58"
        assert result[1]["operationAmount"]["currency"]["code"] == "USD"


def test_file_read_permission_error():
    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open") as mock_open_file:
        mock_is_file.return_value = True
        mock_open_file.side_effect = PermissionError("No read permission")
        result = load_transactions("protected.json")
        assert result == []


def test_corrupted_data_inside_list():
    test_data = [
        {"valid": "data", "operationAmount": {"amount": "100", "currency": "RUB"}},
        {"broken": "data", "operationAmount": "invalid"},  # Некорректный формат
        {"missing_fields": {"amount": 100}},  # Нет currency
        "not_a_dict"
    ]

    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open", mock_open(read_data=json.dumps(test_data))):
        mock_is_file.return_value = True
        result = load_transactions("corrupted.json")
        assert len(result) == 1
        assert result[0]["valid"] == "data"


def test_large_numbers_handling():
    test_data = [
        {
            "id": 939719570,
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD"}
            }
        }
    ]

    with patch("pathlib.Path.is_file") as mock_is_file, \
         patch("pathlib.Path.open", mock_open(read_data=json.dumps(test_data))):
        mock_is_file.return_value = True
        result = load_transactions("large_numbers.json")
        assert result[0]["operationAmount"]["amount"] == "9824.07"
