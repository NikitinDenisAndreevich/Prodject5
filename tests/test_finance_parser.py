import contextlib
import logging
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.finance_parser import read_csv_transactions, read_excel_transactions


# Тест для CSV
@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictReader")
def test_csv_reader(mock_reader, mock_file):
    mock_reader.return_value = [
        {'id': '1', 'amount': '100.0', 'date': '2023-01-01', 'description': 'Payment'},
        {},  # Пустая строка
        {'id': 'invalid', 'amount': 'text', 'date': '', 'description': ''}  # Ошибка
    ]

    with patch.object(logging, 'warning') as mock_warn, \
         patch.object(logging, 'error') as mock_error:
        result = read_csv_transactions("dummy.csv")

    assert len(result) == 1
    mock_warn.assert_called_once_with("CSV: Пустая строка 2 пропущена")
    mock_error.assert_called_once_with("CSV: Ошибка в строке 3: invalid literal for int() with base 10: 'invalid'")


# Тест для Excel
@patch("pandas.read_excel")
def test_excel_reader(mock_excel):
    mock_df = MagicMock()
    mock_df.iterrows.return_value = [
        (0, pd.Series({'id': 1, 'amount': 200.0, 'date': '2023-01-01', 'description': 'Sale'})),
        (1, pd.Series({})),  # Пустая строка
        (2, pd.Series({'id': 3, 'amount': 'invalid', 'date': None, 'description': None}))  # Ошибка
    ]
    mock_excel.return_value = mock_df

    with patch.object(logging, 'warning') as mock_warn, \
         patch.object(logging, 'error') as mock_error:
        result = read_excel_transactions("dummy.xlsx")

    assert len(result) == 1
    mock_warn.assert_called_once_with("Excel: Пустая строка 3 пропущена")
    mock_error.assert_called_once_with("Excel: Ошибка в строке 4: could not convert string to float: 'invalid'")


# Тест отсутствия файла
def test_file_not_found():
    with pytest.raises(FileNotFoundError), \
         patch.object(logging, 'error') as mock_error:
        read_csv_transactions("non_existent.csv")
    mock_error.assert_called_once_with("CSV файл не найден")


# Параметризованный тест пустых файлов
@pytest.mark.parametrize("file_type,func,patcher,expected_log", [
    ("csv", read_csv_transactions, [
        patch("builtins.open", mock_open(read_data="")),
        patch("csv.DictReader", return_value=[])
    ], "CSV"),
    ("xlsx", read_excel_transactions, [
        patch("pandas.read_excel", return_value=pd.DataFrame())
    ], "Excel")
])
def test_empty_files(file_type, func, patcher, expected_log):
    with contextlib.ExitStack() as stack:
        for p in patcher:
            stack.enter_context(p)
        with patch.object(logging, 'info') as mock_info:
            assert len(func(f"empty.{file_type}")) == 0
            mock_info.assert_called_with(f"Успешно загружено 0 транзакций из {expected_log}")
