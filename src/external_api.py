import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://apilayer.com"


def convert_to_rub(transaction: dict) -> float:
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0.0))
    currency = operation_amount.get("currency", {}).get("code", "RUB")
    if currency == "RUB":
        return amount
    if currency in ["USD", "EUR"]:
        if not API_KEY:
            raise ValueError("API_KEY не найден в переменных окружения.")
        headers = {"apikey": API_KEY}
        payload = {"from": currency, "to": "RUB", "amount": amount}
        try:
            response = requests.get(
                BASE_URL, headers=headers, params=payload, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return float(data.get("result", 0.0))
        except (requests.RequestException, KeyError, ValueError):
            return 0.0
    return 0.0
