from datetime import datetime


def filter_by_state(
    dicts_list: list[dict], state: str = "EXECUTED"
) -> list[dict]:
    """Фильтрует список словарей по значению ключа 'state'.
    Функция проходит по каждому словарю в списке и проверяет наличие
    указанного значения состояния в значениях словаря."""

    result = []  # пустой список для результатов
    # Проход по каждому элементу (словарю) в списке
    for item in dicts_list:
        # Проверка наличия искомого состояния в значениях текущего словаря
        if state in item.values():
            result.append(item)  # Добавление совпадающего элемента в результат
    return result


def sort_by_date(data_list: list, reverse: bool = True) -> list:
    """Функция должна возвращать новый список, отсортированный по дате"""
    return sorted(data_list, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
