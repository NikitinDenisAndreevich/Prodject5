import importlib
from unittest.mock import patch

import pytest
import requests


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    """Фикстура для автоматической настройки окружения"""
    monkeypatch.setenv('API_KEY', 'test-key')
    # Перезагружаем модуль для применения изменений в переменных окружения
    import src.external_api
    importlib.reload(src.external_api)


def test_rub_conversion():
    from src.external_api import convert_amount_to_rub
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"}
        }
    }
    assert convert_amount_to_rub(transaction) == 100.50


def test_usd_conversion():
    from src.external_api import convert_amount_to_rub
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
    from src.external_api import convert_amount_to_rub
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
    from src.external_api import convert_amount_to_rub
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "GBP"}
        }
    }
    assert convert_amount_to_rub(transaction) is None


def test_api_failure():
    from src.external_api import convert_amount_to_rub
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
    from src.external_api import convert_amount_to_rub
    transaction = {"operationAmount": {"currency": {"code": "USD"}}}
    assert convert_amount_to_rub(transaction) is None


def test_non_numeric_amount():
    from src.external_api import convert_amount_to_rub
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
            'rates': {'RUB': 75.0},
            'base': 'USD',
            'success': True
        }
        from src.external_api import get_exchange_rate
        rate = get_exchange_rate('USD')
        assert rate == 75.0
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest",
            params={'base': 'USD', 'symbols': 'RUB'},
            headers={'apikey': 'test-key'},
            timeout=10
        )


def test_get_exchange_rate_api_key_missing(monkeypatch):
    monkeypatch.delenv('API_KEY')
    import src.external_api
    importlib.reload(src.external_api)
    from src.external_api import get_exchange_rate
    with pytest.raises(ValueError):
        get_exchange_rate('USD')


def test_get_exchange_rate_network_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.ConnectionError
        from src.external_api import get_exchange_rate
        rate = get_exchange_rate('USD')
        assert rate is None
