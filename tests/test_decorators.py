import os

from src.decorators import log


def test_my_function_with_file():
    @log(filename="mylog.txt")
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)
    assert result == 3
    assert os.path.exists("mylog.txt")

    with open("mylog.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "Функция my_function ок. Результат: 3" in content

    os.remove("mylog.txt")


def test_my_function_without_file():
    @log()
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)
    assert isinstance(result, str)
    assert "Функция my_function ок. Результат: 3" in result


def test_second_fun_error():
    @log(filename="errorlog.txt")
    def second_fun(x, y):
        return x / y

    result = second_fun(1, 0)
    assert "Ошибка записана в errorlog.txt" in result

    with open("errorlog.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "division by zero" in content

    os.remove("errorlog.txt")
