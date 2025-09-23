import re
from collections import defaultdict
from datetime import datetime
from typing import List, Dict


def filter_by_state(data: List[Dict], state: str) -> List[Dict]:
    """Фильтрация транзакций по статусу с приведением к верхнему регистру"""
    target_state = state.upper()
    return [
        tx for tx in data
        if isinstance(tx.get('state'), str)
           and tx['state'].upper() == target_state
    ]


def sort_by_date(data: List[Dict], reverse: bool = False) -> List[Dict]:
    """Сортировка транзакций по дате с обработкой исключений"""

    def get_date(tx):
        date_str = tx.get('date', '')
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            return datetime.min

    return sorted(data, key=get_date, reverse=reverse)


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Поиск транзакций по ключевому слову с использованием regex"""
    try:
        pattern = re.compile(re.escape(search), re.IGNORECASE)
        return [
            tx for tx in data
            if isinstance(tx.get('description'), str)
               and pattern.search(tx['description'])
        ]
    except re.error:
        return data


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Подсчет операций по категориям с сохранением оригинального регистра"""
    category_counts = defaultdict(int)
    normalized_mapping = {c.lower(): c for c in categories}

    for tx in data:
        description = tx.get('description', '').lower()
        if description in normalized_mapping:
            original_category = normalized_mapping[description]
            category_counts[original_category] += 1

    return dict(category_counts)
