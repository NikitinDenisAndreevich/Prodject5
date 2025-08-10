# Импорт необходимых библиотек и модулей
import pytest
from src.processing import filter_by_state, sort_by_date  # Функции, которые тестируем

# Фикстура для общих тестовых данных
@pytest.fixture
def test_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
    ]

# Тестирование функции filter_by_state с разными параметрами состояния (state)
@pytest.mark.parametrize(
    "state, expected_result",
    [
        # Тест-кейс 1: фильтрация по состоянию "EXECUTED"
        ("EXECUTED", [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
        ]),
        # Тест-кейс 2: фильтрация по состоянию "CANCELED"
        ("CANCELED", [
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
        ])
    ]
)
def test_filter_by_state(test_data, state, expected_result):
    """Проверяет фильтрацию операций по заданному состоянию."""
    assert filter_by_state(test_data, state) == expected_result  # Сравниваем результат функции с ожидаемым

def test_filter_by_state_default(test_data):
    """Проверяет поведение функции filter_by_state по умолчанию (без указания состояния)."""
    # Ожидается, что при вызове без параметра state функция вернет все операции со state="EXECUTED"
    assert filter_by_state(test_data) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
    ]

@pytest.mark.parametrize(
    "reverse, expected_result",
    [
        # Тест 1: сортировка по УБЫВАНИЮ (reverse=True)
        (True, [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
        ]),
        # Тест 2: сортировка по ВОЗРАСТАНИЮ (reverse=False)
        (False, [
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}
        ])
    ]
)
def test_sort_by_date(test_data, reverse, expected_result):
    # Вызов тестируемой функции
    sorted_data = sort_by_date(test_data, reverse=reverse)

    # Проверка результата
    assert sorted_data == expected_result
