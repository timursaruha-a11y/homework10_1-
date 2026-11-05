import json
from unittest.mock import patch, mock_open
import pytest
import requests
from src.utils import zip_transactions_from_json
from src.external_api import convert_to_rub

@patch('pathlib.Path.exists', return_value=True)
def test_zip_transactions_success(mock_exists):
    mock_data = [{'id': 1, 'state': 'EXECUTED'}]
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
        assert zip_transactions_from_json('dummy_path.json') == mock_data

def test_zip_transactions_file_not_found():
    with patch('pathlib.Path.exists', return_value=False):
        assert zip_transactions_from_json('missing.json') == []

@patch('pathlib.Path.exists', return_value=True)
def test_zip_transactions_invalid_json(mock_exists):
    with patch('builtins.open', mock_open(read_data='invalid json')):
        assert zip_transactions_from_json('corrupt.json') == []

@patch('pathlib.Path.exists', return_value=True)
def test_zip_transactions_not_a_list(mock_exists):
    with patch('builtins.open', mock_open(read_data=json.dumps({'key': 'value'}))):
        assert zip_transactions_from_json('object.json') == []

def test_convert_to_rub_already_rub():
    transaction = {'operationAmount': {'amount': '150.50', 'currency': {'code': 'RUB'}}}
    assert convert_to_rub(transaction) == 150.50

@patch('src.external_api.requests.get')
def test_convert_to_rub_usd_success(mock_get):
    transaction = {'operationAmount': {'amount': '100.00', 'currency': {'code': 'USD'}}}
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'result': 7500.0}
    assert convert_to_rub(transaction) == 7500.0

@patch('src.external_api.requests.get')
def test_convert_to_rub_api_error(mock_get):
    transaction = {'operationAmount': {'amount': '100.00', 'currency': {'code': 'EUR'}}}
    mock_get.side_effect = requests.RequestException('Ошибка')
    assert convert_to_rub(transaction) == 0.0
