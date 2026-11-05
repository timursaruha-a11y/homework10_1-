import pytest
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    """Тестовый массив транзакций."""
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "operationAmount": {"currency": {"name": "USD", "code": "USD"}},
        },
        {
            "id": 2,
            "description": "Перевод частному лицу",
            "operationAmount": {"currency": {"name": "руб.", "code": "RUB"}},
        },
        {
            "id": 3,
            "description": "Покупка авиабилетов",
            "operationAmount": {"currency": {"name": "USD", "code": "USD"}},
        },
    ]


def test_filter_by_currency(sample_transactions):
    """Тестирует фильтрацию транзакций по валюте."""
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 2
    assert usd_transactions[0]["id"] == 1
    assert usd_transactions[1]["id"] == 3

    rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
    assert len(rub_transactions) == 1
    assert rub_transactions[0]["id"] == 2


def test_transaction_descriptions(sample_transactions):
    """Тестирует генератор описаний транзакций."""
    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions == ["Перевод организации", "Перевод частному лицу", "Покупка авиабилетов"]


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (99999, 100001, ["0000 0000 0009 9999", "0000 0000 0010 0000", "0000 0000 0010 0001"]),
    ],
)
def test_card_number_generator(start, end, expected):
    """Тестирует генерацию диапазонов номеров карт."""
    assert list(card_number_generator(start, end)) == expected
