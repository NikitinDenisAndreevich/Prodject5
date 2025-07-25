def get_mask_card_number(number_card: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX."""
    masked = []
    for i, char in enumerate(number_card):
        if i < 6 or i >= 12:  # Первые 4 и последние 4 цифры
            masked.append(char)
        else:  # Остальные цифры
            masked.append("*")

    # Добавляем пробелы после каждых 4 цифр
    result = ""
    for j, char in enumerate(masked):
        result += char
        if (j + 1) % 4 == 0 and j != len(masked) - 1:
            result += " "

    return result


def get_mask_account(number_card: str) -> str:
    """принимает на вход номер счета и возвращает его маску.
     Номер счета замаскирован и отображается в формате **XXXX"""

    result = ""
    for n in range(-6, 0):
        if n < -4:
            result += "*"
        else:
            result += number_card[n]

    return result
