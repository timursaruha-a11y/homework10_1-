from typing import Union


def get_mask_card_number(number_card: Union[int, str]) -> str:
    """Функция получает на входе номер карты,
    возвращает строковое значение где цифры разбиты в группы по 4 и все
    кроме первых 6-ти и последних 4-х цифрах карыты заменены на *"""
    mask_card = []
    number_card = str(number_card)
    number_card_asterix = ""
    for number in number_card:
        if (
            len(number_card_asterix) < 6
            or len(number_card_asterix) > len(number_card) - 5
        ):
            number_card_asterix += number
        else:
            number_card_asterix += "*"
    start_index_of_interval = 0
    for index in range(0, len(number_card_asterix) + 1, 4):
        mask_card.append(number_card_asterix[start_index_of_interval:index])
        start_index_of_interval = index
    return " ".join(mask_card)


def get_mask_account(accaut_number: Union[int, str]) -> str:
    """Функция получает на входе номер счета и
    возвращает ** и последние 4 цифры счета *"""
    return "**" + str(accaut_number)[-4:]
