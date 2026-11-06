import os
import pytest
from src.decorators import log


# Тестовые функции для проверки декоратора
@log()
def add_numbers(x: int, y: int) -> int:
    """Успешная функция."""
    return x + y


@log()
def divide_numbers(x: int, y: int) -> float:
    """Функция, которая может вызвать ошибку ZeroDivisionError."""
    return x / y


def test_log_console_success(capsys):
    """Тестирует успешное логирование в консоль."""
    result = add_numbers(3, 5)
    assert result == 8

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()
    assert captured.out == "add_numbers ok\n"


def test_log_console_error(capsys):
    """Тестирует логирование ошибки в консоль."""
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()
    assert "divide_numbers error: ZeroDivisionError. Inputs: (10, 0), {}" in captured.out


def test_log_file_success(tmp_path):
    """Тестирует успешное логирование в файл."""
    # Создаем путь к временному файлу
    test_file = tmp_path / "test_success.log"
    file_path = str(test_file)

    @log(filename=file_path)
    def multiply(x: int, y: int) -> int:
        return x * y

    assert multiply(4, 5) == 20

    # Проверяем содержимое файла
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "multiply ok\n"


def test_log_file_error(tmp_path):
    """Тестирует логирование ошибки в файл."""
    test_file = tmp_path / "test_error.log"
    file_path = str(test_file)

    @log(filename=file_path)
    def faulty_func():
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError):
        faulty_func()

    # Проверяем содержимое файла
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "faulty_func error: ValueError. Inputs: (), {}" in content