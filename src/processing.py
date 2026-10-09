from typing import Any


def filter_by_state(
    list_of_dict: list[dict[Any, Any]], state: str = "EXECUTED"
) -> list[dict[Any, Any]]:
    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
    state соответствует указанному значению"""
    return [item for item in list_of_dict if item["state"] == state]


def sort_by_date(
    list_of_dict: list[dict[Any, Any]], date_reverse: bool = False
) -> list[dict[Any, Any]]:
    """Возвращает список отсортированныц по параметру date, принимает необязательный параметр date_reverse"""
    return sorted(list_of_dict, key=lambda item: item["date"], reverse=date_reverse)
