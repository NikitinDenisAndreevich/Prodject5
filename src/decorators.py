import time


def log(filename=None):
    """Декоратор для логирования выполнения функций и обработки ошибок.

    Если указан filename, логи записываются в файл. Иначе возвращаются строкой.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                log_message = (
                    f"Начало: {start_time}\n"
                    f"Функция {func.__name__} ок. Результат: {result}\n"
                    f"Конец: {end_time}\n"
                )

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                    return result
                return log_message

            except Exception as e:
                error_message = (
                    f"{func.__name__} error: {e}\n"
                    f"Inputs: args={args}, kwargs={kwargs}\n"
                )

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(error_message)
                    return f"Ошибка записана в {filename}"
                return error_message

        return wrapper

    return decorator
