# Виджет "Последние операции" для личного кабинета банка

![Bank Operations Widget](https://i.ibb.co/cKc5xdtL/Shutterstock-1900200.png)

## Описание проекта
Программа для отображения последних банковских операций клиента в личном кабинете. 
Проект разрабатывается для IT-отдела крупного банка в рамках модернизации клиентского портала.

## Основной функционал
### ![.](https://i.ibb.co/FqhDh1pq/shield-clipart-lg-2.png) Маскирование данных
- src/masks.py `get_mask_card_number(number: str) -> str`  
  Маскирует номер карты: `XXXX XX** **** XXXX`  
  Пример: `"7000792289606361" -> "7000 79** **** 6361"`

- src/masks.py `get_mask_account(number: str) -> str`  
  Маскирует номер счета: `**XXXX`  
  Пример: `"73654108430135874305" -> "**4305"`

- src/widget.py `mask_account_card(number: str) -> str`  
  Автоматически определяет тип номера (карта/счет) и применяет соответствующую маскировку

### ![.](https://i.ibb.co/qM0S8BYK/images.png) Работа с датами
- src/widget.py `get_date(date_str: str) -> str`  
  Конвертирует дату из формата `"2024-03-11T02:26:18.671407"` в `"11.03.2024"`

### ![.](https://i.ibb.co/v4KmGbDN/8668568.png) Фильтрация и сортировка
- src/widget.py `filter_by_state(operations: list, state: str = "EXECUTED") -> list`  
  Фильтрует операции по статусу (по умолчанию: "EXECUTED")

- src/widget.py `sort_by_date(operations: list, reverse: bool = True) -> list`  
  Сортирует операции по дате (по умолчанию: от новых к старым)

### ![.](https://i.ibb.co/XfkHrdsZ/New-Template-Photoroom.png) Генераторы
- src/generators.py `filter_by_currency(transactions: list, currency: str) -> Iterator[dict]`  
Фильтрует транзакции по коду валюты.

- src/generators.py `transaction_descriptions(transactions: list) -> Iterator[str]`  
  Возвращает итератор с описаниями транзакций.

- src/generators.py `card_number_generator(begin: int, end: int) -> Iterator[str]`
Генерирует номера карт в формате 16 цифр с ведущими нулями.

## ![.](https://i.ibb.co/QxSg4m1/images-Photoroom.png) Парсинг финансовых данных

Модуль `finance_parser.py` отвечает за чтение и предобработку транзакций из файлов.

### Основные функции:
- **`read_csv_transactions(file_path: str) -> list[dict]`**  
  Читает CSV-файл с транзакциями и возвращает список словарей.  
  **Формат CSV:**
  ```csv
  id,date,amount,currency,description,from,to,status
  1,2024-03-11T02:26:18.671407,100.0,USD,Payment,Счет **1234,Visa 1234 56** **** 5678,EXECUTED
  

### В папке tests подготовлены тесты ([test_masks.py](tests%2Ftest_masks.py), [test_processing.py](tests%2Ftest_processing.py), [test_widget.py](tests%2Ftest_widget.py), [test_generators.py](tests%2Ftest_generators.py), [test_utils.py](tests%2Ftest_utils.py), [test_finance_parser.py](tests%2Ftest_finance_parser.py), [test_external_api.py](tests%2Ftest_external_api.py), [test_decorators.py](tests%2Ftest_decorators.py))
Функциональный код покрыт тестами на 92% на 05.09.2025г.
### начало работы с программой
1. git clone git@github.com:NikitinDenisAndreevich/Prodject5.git # Сконирование программы 
2. poetry install # установка зависимостей