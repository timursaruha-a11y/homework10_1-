from unittest.mock import patch

import requests

from src.external_api import convert_to_rub


@patch("src.external_api.requests.get")
def test_convert_to_rub_usd_success(mock_get):
    """Тест успешной конвертации USD в RUB."""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    # Настраиваем мок для requests.get
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7400.0}  # Имитируем ответ от API

    # Проверяем, что функция возвращает корректную сумму
    assert convert_to_rub(transaction) == 7400.0


@patch("src.external_api.requests.get")
def test_convert_to_rub_api_error(mock_get):
    """Тест обработки ошибки API при конвертации."""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "EUR"}}}

    # Имитируем исключение при запросе
    mock_get.side_effect = requests.RequestException("Ошибка соединения")

    # Функция должна безопасно вернуть 0.0
    assert convert_to_rub(transaction) == 0.0
