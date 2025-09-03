import json
import logging
from pathlib import Path
from typing import Any, Dict, List

# Настройка логгера для модуля utils
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

logger.debug("Тестовый DEBUG-лог")
logger.info("Тестовый INFO-лог")

file_handler = logging.FileHandler('utils.log', encoding='utf-8')
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """
    Загружает финансовые транзакции из JSON-файла с валидацией структуры.
    Обрабатывает основные файловые ошибки и ошибки формата данных.
    """
    path = Path(file_path)
    logger.debug(f"Попытка загрузки файла: {path}")

    try:
        if not path.is_file():
            logger.warning(f"Файл не найден: {path}")
            return []

        if not path.exists():
            logger.error(f"Путь не существует: {path}")
            return []

        with path.open(encoding='utf-8') as f:
            logger.debug(f"Открытие файла: {path}")
            data = json.load(f)
            logger.info(f"Успешно загружено {len(data)} записей из {path}")

        valid_transactions = [
            item for item in data
            if isinstance(item, dict)
            and isinstance(item.get("operationAmount"), dict)
            and "amount" in item["operationAmount"]
            and "currency" in item["operationAmount"]
        ]

        logger.debug(f"Найдено {len(valid_transactions)} валидных транзакций")
        return valid_transactions

    except (FileNotFoundError, json.JSONDecodeError,
            UnicodeDecodeError, PermissionError) as e:
        logger.error(f"Ошибка при обработке файла {path}: {str(e)}", exc_info=True)
        return []
