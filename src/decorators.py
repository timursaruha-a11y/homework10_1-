from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор, который логирует начало, конец, результат работы функции или ошибку.

    Если filename задан, пишет в файл. Если нет — выводит в консоль (print).
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успешном выполнении
                log_message = f"{func.__name__} ok\n"

                # Записываем лог
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")

                return result

            except Exception as e:
                # Формируем сообщение об ошибке с именем, типом ошибки и параметрами
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                # Записываем лог ошибки
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")

                # Пробрасываем ошибку дальше, чтобы не ломать логику программы
                raise e

        return wrapper

    return decorator
