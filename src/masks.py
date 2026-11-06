import logging
import os
from typing import Union

# Получаем путь к корню проекта и создаем папку logs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Создаем логер для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Настраиваем запись в файл masks.log в режиме перезаписи ('w')
log_file = os.path.join(LOGS_DIR, "masks.log")
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")

# Формат: метка времени, название модуля, уровень серьезности, сообщение
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_mask_card_number(number_card: Union[int, str]) -> str:
    """Функция получает на входе номер карты,
    возвращает строковое значение где цифры разбиты в группы по 4 и все
    кроме первых 6-ти и последних 4-х цифрах карыты заменены на *"""
    logger.info(f"Начало маскирования номера карты: {number_card}")

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

    result = " ".join(mask_card)
    logger.info("Номер карты успешно замаскирован")
    return result


def get_mask_account(accaut_number: Union[int, str]) -> str:
    """Функция получает на входе номер счета и
    возвращает ** и последние 4 цифры счета *"""
    logger.info(f"Начало маскирования номера счета: {accaut_number}")

    result = "**" + str(accaut_number)[-4:]
    logger.info("Номер счета успешно замаскирован")
    return result
