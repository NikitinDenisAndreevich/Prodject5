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

- `sort_by_date(operations: list, reverse: bool = True) -> list`  
  Сортирует операции по дате (по умолчанию: от новых к старым)
