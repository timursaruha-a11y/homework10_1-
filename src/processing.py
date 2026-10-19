from typing import Any


def filter_by_state(
    list_of_dict: list[dict[Any, Any]], state: str = "EXECUTED"
) -> list[dict[Any, Any]]:
    """Возвращает новый список словарей.

    Содержит только те словари, у которых ключ state соответствует указанному значению.
    """
    return [item for item in list_of_dict if item.get("state") == state]


def sort_by_date(
    list_of_dict: list[dict[Any, Any]], date_reverse: bool = True
) -> list[dict[Any, Any]]:
    """Возвращает список, отсортированный по параметру date.

    Принимает необязательный параметр date_reverse (по умолчанию True — убывание).
    """
    return sorted(
        list_of_dict, key=lambda item: item.get("date", ""), reverse=date_reverse
    )

