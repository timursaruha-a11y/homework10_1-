from unittest.mock import patch, MagicMock
import requests
from src.external_api import get_exchange_amount


# Тест с моком для API-запроса
@patch('requests.request')
@patch('os.getenv')
def test_get_exchange_amount_success(mock_getenv, mock_request):
    # Мокаем os.getenv для получения API_KEY из переменных окружения
    mock_getenv.return_value = 'test_api_key'

    # Мокаем ответ от requests.request
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 74.0}  # Мокаем результат API-конвертации
    mock_request.return_value = mock_response

    # Вызываем функцию с тестовыми значениями
    result = get_exchange_amount('USD', '100')

    # Проверяем, что возвращаемое значение правильное
    assert result == 74.0

    # Проверяем, что запрос был сделан с правильными параметрами
    mock_request.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": 'test_api_key'},
        params={"amount": '100', "from": 'USD', "to": 'RUB'}
    )


# Тест на случай, если API возвращает ошибку
@patch('requests.request')
@patch('os.getenv')
def test_get_exchange_amount_api_error(mock_getenv, mock_request):
    mock_getenv.return_value = 'test_api_key'

    # Мокаем случай, когда API возвращает ошибку
    mock_response = MagicMock()
    mock_response.json.return_value = {}  # Пустой ответ, нет ключа "result"
    mock_request.return_value = mock_response

    # Проверяем, что функция возвращает None или генерирует исключение
    result = get_exchange_amount('USD', '100')
    assert result is None  # Так как нет ключа "result" в ответе