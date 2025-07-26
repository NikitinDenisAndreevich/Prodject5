from . import masks


def mask_account_card(card: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа
    """

    # Ключевое слово для идентификации типа "Счет"
    test_word = "счет"

    # Разбиваем строку на составляющие слова
    card_parts = card.lower().split()

    # Инициализируем переменную для результата
    masked_result = ""

    if test_word in card_parts:
        # Маскировка для карты (берем последние 16 символов)
        masked_number = masks.get_mask_account(card[-20:])
        masked_result = card[:-20] + masked_number
    else:
        # Маскировка для счета (берем последние 20 символов)
        masked_number = masks.get_mask_card_number(card[-16:])
        masked_result = card[:-16] + masked_number

    return masked_result


def get_date(date: str) -> str:
    """функция меняет формат даты.
    Принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ"("11.03.2024")
    """
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    return f"{day}.{month}.{year}"
