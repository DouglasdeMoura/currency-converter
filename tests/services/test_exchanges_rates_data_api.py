import pytest
from requests import HTTPError

from currency_converter.services.exchanges_rates_data_api import get_latest  # Replace with the actual module name


def test_get_latest_success(requests_mock):
    # Mock the API endpoint with a successful response
    url = "https://api.apilayer.com/exchangerates_data/latest"
    mock_response = {
        "base": "EUR",
        "date": "2024-08-12",
        "rates": {"BRL": 6.015443, "EUR": 1, "JPY": 161.21704, "USD": 1.092168},
        "success": True,
        "timestamp": 1723462876,
    }
    requests_mock.get(url, json=mock_response, status_code=200)

    response = get_latest()

    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_response


def test_get_latest_failure(requests_mock):
    # Mock the API endpoint with a failed response
    url = "https://api.apilayer.com/exchangerates_data/latest"
    requests_mock.get(url, status_code=404)

    with pytest.raises(HTTPError):
        get_latest()


def test_get_latest_with_default_arguments(requests_mock):
    # Mock the API endpoint
    url = "https://api.apilayer.com/exchangerates_data/latest"
    requests_mock.get(url, status_code=200, json={})

    get_latest()

    # Verify that the correct URL was requested
    assert requests_mock.called
    request = requests_mock.request_history[0]
    assert request.url == f"{url}?base=EUR&symbols=BRL%2CUSD%2CEUR%2CJPY"  # The symbols should be URL-encoded
    assert request.headers["apikey"] == "test_api_key"  # Ensure the correct API key was used


def test_get_latest_with_custom_arguments(requests_mock):
    # Mock the API endpoint
    url = "https://api.apilayer.com/exchangerates_data/latest"
    requests_mock.get(url, status_code=200, json={})

    get_latest(base_currency="USD", symbols="EUR,GBP")

    # Verify that the correct URL was requested
    assert requests_mock.called
    request = requests_mock.request_history[0]
    assert request.url == f"{url}?base=USD&symbols=EUR%2CGBP"  # The symbols should be URL-encoded
    assert request.headers["apikey"] == "test_api_key"  # Ensure the correct API key was used
