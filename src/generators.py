from typing import Any, Dict, Iterator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str
) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по заданной валюте и возвращает итератор."""
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        if currency_info.get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Возвращает описание каждой операции по очереди."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генерирует номера карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне."""
    for number in range(start, end + 1):
        # Превращаем число в строку длиной 16 символов, заполняя нулями слева
        num_str = f"{number:016d}"
        # Разрезаем на 4 блока по 4 цифры и соединяем пробелами
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"
