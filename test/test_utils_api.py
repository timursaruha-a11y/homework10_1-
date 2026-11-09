import json
from unittest.mock import MagicMock, mock_open, patch

import requests

from src.external_api import convert_to_rub
from src.utils import (
    read_transactions_csv,
    read_transactions_excel,
    zip_transactions_from_json,
)

# --- Твои существующие тесты для JSON и API ---


@patch("pathlib.Path.exists", return_value=True)
def test_zip_transactions_success(mock_exists):
    mock_data = [{"id": 1, "state": "EXECUTED"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        assert zip_transactions_from_json("dummy_path.json") == mock_data


def test_zip_transactions_file_not_found():
    with patch("pathlib.Path.exists", return_value=False):
        assert zip_transactions_from_json("missing.json") == []


@patch("pathlib.Path.exists", return_value=True)
def test_zip_transactions_invalid_json(mock_exists):
    with patch("builtins.open", mock_open(read_data="invalid json")):
        assert zip_transactions_from_json("corrupt.json") == []


@patch("pathlib.Path.exists", return_value=True)
def test_zip_transactions_not_a_list(mock_exists):
    with patch("builtins.open", mock_open(read_data=json.dumps({"key": "value"}))):
        assert zip_transactions_from_json("object.json") == []


def test_convert_to_rub_already_rub():
    transaction = {"operationAmount": {"amount": "150.50", "currency": {"code": "RUB"}}}
    assert convert_to_rub(transaction) == 150.50


@patch("src.external_api.requests.get")
def test_convert_to_rub_usd_success(mock_get):
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.0}
    assert convert_to_rub(transaction) == 7500.0


@patch("src.external_api.requests.get")
def test_convert_to_rub_api_error(mock_get):
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "EUR"}}}
    mock_get.side_effect = requests.RequestException("Ошибка")
    assert convert_to_rub(transaction) == 0.0


# --- Новые тесты для функций чтения CSV и Excel ---


@patch("pathlib.Path.exists", return_value=True)
@patch("pandas.read_csv")
def test_read_transactions_csv_success(mock_read_csv, mock_exists):
    """Тест успешного чтения CSV файла через мок pandas."""
    # Создаем фейковый DataFrame, который вернет pandas
    mock_df = MagicMock()
    mock_df.fillna.return_value.to_dict.return_value = [{"id": 1, "state": "EXECUTED"}]
    mock_read_csv.return_value = mock_df

    assert read_transactions_csv("dummy.csv") == [{"id": 1, "state": "EXECUTED"}]


def test_read_transactions_csv_file_not_found():
    """Тест возврата пустого списка, если CSV файл не существует."""
    with patch("pathlib.Path.exists", return_value=False):
        assert read_transactions_csv("missing.csv") == []


@patch("pathlib.Path.exists", return_value=True)
@patch("pandas.read_csv")
def test_read_transactions_csv_error(mock_read_csv, mock_exists):
    """Тест возврата пустого списка при ошибке парсинга CSV."""
    mock_read_csv.side_effect = Exception("Ошибка чтения")
    assert read_transactions_csv("corrupt.csv") == []


@patch("pathlib.Path.exists", return_value=True)
@patch("pandas.read_excel")
def test_read_transactions_excel_success(mock_read_excel, mock_exists):
    """Тест успешного чтения Excel файла через мок pandas."""
    mock_df = MagicMock()
    mock_df.fillna.return_value.to_dict.return_value = [{"id": 2, "state": "CANCELED"}]
    mock_read_excel.return_value = mock_df

    assert read_transactions_excel("dummy.xlsx") == [{"id": 2, "state": "CANCELED"}]


def test_read_transactions_excel_file_not_found():
    """Тест возврата пустого списка, если Excel файл не существует."""
    with patch("pathlib.Path.exists", return_value=False):
        assert read_transactions_excel("missing.xlsx") == []


@patch("pathlib.Path.exists", return_value=True)
@patch("pandas.read_excel")
def test_read_transactions_excel_error(mock_read_excel, mock_exists):
    """Тест возврата пустого списка при ошибке парсинга Excel."""
    mock_read_excel.side_effect = Exception("Ошибка чтения")
    assert read_transactions_excel("corrupt.xlsx") == []
