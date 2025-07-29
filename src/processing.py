from widget import get_date


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


def sort_by_date(dicts_list: list[dict], reverse_order=True) -> list[dict]:
    """
    Сортирует список словарей по дате в указанном порядке."""
    result = []  # пустой список для результатов
    correct_date = {}  # пустой словарь для проверки
    i = 0  # для записи индекса словаря изначального
    x = 0  # временная переменная
    sorted_keys = []  # временная переменная для отсортировски
    for dict in dicts_list:
        result = get_date(dict["date"]).split('.')
        x = int(result[0]) + int(result[1]) * 31 + int(result[2]) * 365
        correct_date[i] = x
        i += 1
    # Сортируем индексы словаря
    sorted_keys = [key for key, value in sorted(correct_date.items(), key=lambda x: x[1])]
    result = []
    if reverse_order is True:
        for y in sorted_keys:
            result.append(dicts_list[y])
    elif reverse_order is False:
        for y in reversed(sorted_keys):
            result.append(dicts_list[y])
    return result
