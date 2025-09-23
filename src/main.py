from pathlib import Path
from src import utils, processing, widget


def get_file_path(extension: str) -> Path:
    """Получение корректного пути к файлу"""
    while True:
        file_name = input("Введите имя файла: ").strip()
        path = Path('data') / file_name

        if not path.exists():
            print(f"Файл {path} не найден")
            continue

        if path.suffix.lower() != f".{extension}":
            print(f"Ожидается файл с расширением.{extension}")
            continue

        return path


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор типа файла
    file_type = input(
        "Выберите тип файла:\n1. JSON\n2. CSV\n3. XLSX\n> "
    ).strip()

    file_types = {
        '1': ('json', utils.load_json_transactions),
        '2': ('csv', utils.load_csv_transactions),
        '3': ('xlsx', utils.load_excel_transactions)
    }

    if file_type not in file_types:
        print("Неверный выбор типа файла")
        return

    ext, loader = file_types[file_type]
    print(f"\nДля обработки выбран {ext.upper()}-файл.")

    # Загрузка данных
    while True:
        try:
            path = get_file_path(ext)
            data = loader(path)

            if not data:
                print("Файл не содержит валидных транзакций. Проверьте формат данных.")
                continue

            break
        except Exception as e:
            print(f"Ошибка загрузки: {str(e)}")

    # Фильтрация по статусу
    valid_statuses = {'EXECUTED', 'CANCELED', 'PENDING'}
    while True:
        status = input(
            "\nВведите статус операций (EXECUTED/CANCELED/PENDING): "
        ).upper()
        if status in valid_statuses:
            filtered_data = processing.filter_by_state(data, status)
            print(f"Найдено {len(filtered_data)} операций со статусом '{status}'")
            break
        print(f"Статус '{status}' недоступен. Попробуйте снова.")

    # Дополнительные фильтры
    if input("\nОтсортировать операции по дате? (да/нет): ").lower() == 'да':
        reverse = input("Сортировать по убыванию? (да/нет): ").lower() == 'да'
        filtered_data = processing.sort_by_date(filtered_data, reverse)

    if input("\nПоказывать только рублевые транзакции? (да/нет): ").lower() == 'да':
        filtered_data = [tx for tx in filtered_data if tx.get('currency') == 'RUB']

    if input("\nИскать по ключевому слову в описании? (да/нет): ").lower() == 'да':
        search = input("Введите поисковый запрос: ").strip()
        filtered_data = processing.process_bank_search(filtered_data, search)

    # Вывод результатов
    print(f"\n{'=' * 40}\nИтоговый список транзакций ({len(filtered_data)} шт.):")
    for i, tx in enumerate(filtered_data, 1):
        print(f"\n{i}. {widget.format_transaction(tx)}")


if __name__ == "__main__":
    main()