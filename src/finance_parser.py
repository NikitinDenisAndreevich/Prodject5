import csv
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)


def read_csv_transactions(file_path: str) -> list[dict]:
    """
    Читает транзакции из CSV-файла.
    Пропускает пустые строки и некорректные данные.
    """
    transactions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, 1):
                if not row or all(v.strip() == '' for v in row.values()):
                    logging.warning(f"CSV: Пустая строка {i} пропущена")
                    continue
                try:
                    transactions.append({
                        'id': int(row['id']),
                        'amount': float(row['amount']),
                        'date': row['date'],
                        'description': row['description']
                    })
                except (KeyError, ValueError) as e:
                    logging.error(f"CSV: Ошибка в строке {i}: {e}")
        logging.info(f"Успешно загружено {len(transactions)} транзакций из CSV")
        return transactions
    except FileNotFoundError:
        logging.error("CSV файл не найден")
        raise


def read_excel_transactions(file_path: str) -> list[dict]:
    """
    Читает транзакции из Excel-файла.
    Обрабатывает пустые строки и ошибки данных.
    """
    transactions = []
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        for index, row in df.iterrows():
            if pd.isnull(row).all():
                logging.warning(f"Excel: Пустая строка {index + 2} пропущена")
                continue
            try:
                transactions.append({
                    'id': int(row['id']),
                    'amount': float(row['amount']),
                    'date': str(row['date']),
                    'description': str(row['description'])
                })
            except (KeyError, ValueError) as e:
                logging.error(f"Excel: Ошибка в строке {index + 2}: {e}")
        logging.info(f"Успешно загружено {len(transactions)} транзакций из Excel")
        return transactions
    except FileNotFoundError:
        logging.error("Excel файл не найден")
        raise
