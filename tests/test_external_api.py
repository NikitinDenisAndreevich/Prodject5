import importlib
import json
import os
import tempfile
from unittest.mock import patch

import pytest
import requests

from src.external_api import convert_amount_to_rub, get_exchange_rate, open_json_file


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    """Фикстура для автоматической настройки окружения"""
    monkeypatch.setenv('API_KEY', 'test-key')
    # Перезагружаем модуль для применения изменений в переменных окружения
    import src.external_api
    importlib.reload(src.external_api)


def test_rub_conversion():
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"}
        }
    }
    assert convert_amount_to_rub(transaction) == 100.50


def test_usd_conversion():
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }
    with patch('src.external_api.get_exchange_rate') as mock_rate:
        mock_rate.return_value = 75.50
        assert convert_amount_to_rub(transaction) == 7550.00


def test_eur_conversion():
    transaction = {
        "operationAmount": {
            "amount": "50.00",
            "currency": {"code": "EUR"}
        }
    }
    with patch('src.external_api.get_exchange_rate') as mock_rate:
        mock_rate.return_value = 80.25
        assert convert_amount_to_rub(transaction) == 4012.50


def test_invalid_currency():
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "GBP"}
        }
    }
    assert convert_amount_to_rub(transaction) is None


def test_api_failure():
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }
    with patch('src.external_api.get_exchange_rate') as mock_rate:
        mock_rate.return_value = None
        assert convert_amount_to_rub(transaction) is None


def test_missing_keys():
    transaction = {"operationAmount": {"currency": {"code": "USD"}}}
    assert convert_amount_to_rub(transaction) is None


def test_non_numeric_amount():
    transaction = {
        "operationAmount": {
            "amount": "abc",
            "currency": {"code": "USD"}
        }
    }
    assert convert_amount_to_rub(transaction) is None


def test_get_exchange_rate_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': 75.0,
            'success': True
        }
        rate = get_exchange_rate('USD')
        assert rate == 75.0


def test_get_exchange_rate_api_key_missing(monkeypatch):
    monkeypatch.delenv('API_KEY')
    import src.external_api
    importlib.reload(src.external_api)
    with pytest.raises(ValueError):
        get_exchange_rate('USD')


def test_get_exchange_rate_network_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.ConnectionError
        rate = get_exchange_rate('USD')
        assert rate is None


def test_open_json_file_valid(capsys):
    """Тест корректного JSON-файла"""
    test_data = {"key": "value"}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        json.dump(test_data, tmp, ensure_ascii=False)
        tmp_path = tmp.name

    result = open_json_file(tmp_path)
    assert result == test_data
    captured = capsys.readouterr()
    assert "не найден" not in captured.out
    assert "формата JSON" not in captured.out
    os.unlink(tmp_path)


def test_open_json_file_missing(capsys):
    """Тест отсутствия файла"""
    result = open_json_file("non_existent.json")
    assert result is None
    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_open_json_file_invalid(capsys):
    """Тест некорректного JSON"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp.write("{invalid}")
        tmp_path = tmp.name

    result = open_json_file(tmp_path)
    assert result is None
    captured = capsys.readouterr()
    assert "формата JSON" in captured.out
    os.unlink(tmp_path)


def test_open_json_file_empty(capsys):
    """Тест пустого файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name

    result = open_json_file(tmp_path)
    assert result is None
    captured = capsys.readouterr()
    assert "формата JSON" in captured.out
    os.unlink(tmp_path)
