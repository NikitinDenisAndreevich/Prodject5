import logging

# Настройка логгера для модуля masks
logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('masks.log', encoding='utf-8')
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(number_card: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX."""
    logger.debug(f"Попытка маскировки номера карты: {number_card}")

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

    logger.info(f"Успешная маскировка карты: {result}")
    return result


def get_mask_account(number_account: str) -> str:
    """Принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX"""
    logger.debug(f"Попытка маскировки номера счета: {number_account}")

    result = ""
    try:
        for n in range(-6, 0):
            if n < -4:
                result += "*"
            else:
                result += number_account[n]
        logger.info(f"Успешная маскировка счета: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при маскировке счета: {str(e)}", exc_info=True)
        return ""
