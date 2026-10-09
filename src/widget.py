from src.masks import get_mask_account as account
from src.masks import get_mask_card_number as card


def mask_account_card(data_of_card: str) -> str:
    """Принимает номер карты или номер чсета и возвражает его под маской"""
    if data_of_card.split()[0].lower() == "счет":
        return data_of_card.split()[0] + account(data_of_card.split()[1])
    else:
        return data_of_card.split()[0] + card(data_of_card.split()[1])


def get_date(string_whith_data: str) -> str:
    """Изменяет формат даты"""
    return ".".join(string_whith_data.split("T")[0].split("-")[::-1])
