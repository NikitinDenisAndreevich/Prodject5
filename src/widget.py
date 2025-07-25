from. import masks


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
