import json
import logging
import os
from pathlib import Path

# Получаем путь к корню проекта и создаем папку logs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Создаем логер для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Настраиваем запись в файл utils.log в режиме перезаписи ('w')
log_file = os.path.join(LOGS_DIR, "utils.log")
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")

# Устанавливаем требуемый формат
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def zip_transactions_from_json(file_path: str | Path) -> list[dict]:
    path = Path(file_path)
    logger.info(f"Попытка чтения транзакций из JSON файла по пути: {path}")

    if not path.exists():
        logger.error(f"Файл не найден по пути: {path}")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info(f"Данные успешно прочитаны. Найдено транзакций: {len(data)}")
                return data
            logger.error("Структура JSON некорректна: файл содержит не список (list)")
            return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {path}: {e}")
        return []
    except OSError as e:
        logger.error(f"Ошибка ввода-вывода при работе с файлом {path}: {e}")
        return []
