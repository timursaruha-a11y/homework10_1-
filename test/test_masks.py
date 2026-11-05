import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number, expected_mask",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number(card_number, expected_mask):
    """Тестирует корректность маскирования номеров карт."""
    assert get_mask_card_number(card_number) == expected_mask


@pytest.mark.parametrize(
    "account_number, expected_mask",
    [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
    ],
)
def test_get_mask_account(account_number, expected_mask):
    """Тестирует корректность маскирования номеров счетов."""
    assert get_mask_account(account_number) == expected_mask
