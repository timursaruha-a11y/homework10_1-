import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "data_of_card, expected_result",
    [
        # Обрати внимание: склеивается без пробела, так как в твоем коде написано: ...split()[0] + account(...)
        ("Счет 73654108430135874305", "Счет**4305"),
        ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),
    ],
)
def test_mask_account_card(data_of_card, expected_result):
    """Тестирует маскирование карт и счетов через виджет."""
    assert mask_account_card(data_of_card) == expected_result


def test_get_date():
    """Тестирует форматирование даты из строки ISO в формат ДД.ММ.ГГГГ."""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2023-10-01T12:00:00") == "01.10.2023"
