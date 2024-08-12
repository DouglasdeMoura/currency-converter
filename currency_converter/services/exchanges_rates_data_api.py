import os
from typing import Optional

import requests
from requests import Response

EXCHANGE_BASE_URL = os.getenv("EXCHANGE_BASE_URL")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
HEADERS = {"apikey": EXCHANGE_RATE_API_KEY}


def get_latest(base_currency: str = "EUR", symbols: Optional[str] = "BRL,USD,EUR,JPY") -> Optional[Response]:
    """
    Fetch the latest exchange rates for the specified base currency and symbols.

    :param base_currency: The base currency for the exchange rates.
    :param symbols: A comma-separated list of currency symbols to retrieve rates for.
    :return: A Response object if the request is successful, otherwise None.
    """
    response = requests.get(
        f"{EXCHANGE_BASE_URL}/latest", params={"base": base_currency, "symbols": symbols}, headers=HEADERS
    )
    response.raise_for_status()  # Raise an error for bad status codes
    return response
