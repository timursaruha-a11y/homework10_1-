from typing import Any, Dict, List


def filter_by_state(
    data: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_data = [item for item in data if item.get("state") == state]
    return filtered_data


def sort_by_date(
    data: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу 'date'.

    По умолчанию сортировка идет от самых свежих к самым старым (по убыванию).
    """
    sorted_data = sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)
    return sorted_data
