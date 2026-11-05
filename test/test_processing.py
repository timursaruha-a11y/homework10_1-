import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    """Фикстура, предоставляющая тестовый список банковских операций."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-10-03T15:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-09-25T09:15:00"},
        {"id": 4, "state": "PENDING", "date": "2023-10-02T10:00:00"},
    ]


# Тестирование функции filter_by_state с помощью параметризации
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("NON_EXISTENT", []),  # Проверка несуществующего статуса
    ],
)
def test_filter_by_state(sample_data, state, expected_ids):
    """Тестирует фильтрацию транзакций по разным статусам."""
    result = filter_by_state(sample_data, state)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids


def test_filter_by_state_default(sample_data):
    """Тестирует, что статус по умолчанию 'EXECUTED'."""
    result = filter_by_state(sample_data)
    result_ids = [item["id"] for item in result]
    assert result_ids == [1, 3]


# Тестирование функции sort_by_date с параметризацией направления сортировки
@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [2, 4, 1, 3]),  # По убыванию (от новых к старым)
        (False, [3, 1, 4, 2]),  # По возрастанию (от старых к новым)
    ],
)
def test_sort_by_date(sample_data, reverse, expected_ids):
    """Тестирует сортировку транзакций по дате (в обе стороны)."""
    result = sort_by_date(sample_data, reverse=reverse)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids


def test_sort_by_date_default(sample_data):
    """Тестирует сортировку по умолчанию (по убыванию)."""
    result = sort_by_date(sample_data)
    result_ids = [item["id"] for item in result]
    assert result_ids == [2, 4, 1, 3]
