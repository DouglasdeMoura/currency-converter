import os
from typing import Optional

import requests
from django.core.exceptions import BadRequest
from pydantic import BaseModel
from requests import Response

EXCHANGE_BASE_URL = os.getenv("EXCHANGE_BASE_URL")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
HEADERS = {"apikey": EXCHANGE_RATE_API_KEY}


class Rates(BaseModel):
    AED: Optional[float] = None
    AFN: Optional[float] = None
    ALL: Optional[float] = None
    AMD: Optional[float] = None
    ANG: Optional[float] = None
    AOA: Optional[float] = None
    ARS: Optional[float] = None
    AUD: Optional[float] = None
    AWG: Optional[float] = None
    AZN: Optional[float] = None
    BAM: Optional[float] = None
    BBD: Optional[float] = None
    BDT: Optional[float] = None
    BGN: Optional[float] = None
    BHD: Optional[float] = None
    BIF: Optional[float] = None
    BMD: Optional[float] = None
    BND: Optional[float] = None
    BOB: Optional[float] = None
    BRL: Optional[float] = None
    BSD: Optional[float] = None
    BTC: Optional[float] = None
    BTN: Optional[float] = None
    BWP: Optional[float] = None
    BYN: Optional[float] = None
    BYR: Optional[float] = None
    BZD: Optional[float] = None
    CAD: Optional[float] = None
    CDF: Optional[float] = None
    CHF: Optional[float] = None
    CLF: Optional[float] = None
    CLP: Optional[float] = None
    CNH: Optional[float] = None
    CNY: Optional[float] = None
    COP: Optional[float] = None
    CRC: Optional[float] = None
    CUC: Optional[float] = None
    CUP: Optional[float] = None
    CVE: Optional[float] = None
    CZK: Optional[float] = None
    DJF: Optional[float] = None
    DKK: Optional[float] = None
    DOP: Optional[float] = None
    DZD: Optional[float] = None
    EGP: Optional[float] = None
    ERN: Optional[float] = None
    ETB: Optional[float] = None
    EUR: Optional[float] = None
    FJD: Optional[float] = None
    FKP: Optional[float] = None
    GBP: Optional[float] = None
    GEL: Optional[float] = None
    GGP: Optional[float] = None
    GHS: Optional[float] = None
    GIP: Optional[float] = None
    GMD: Optional[float] = None
    GNF: Optional[float] = None
    GTQ: Optional[float] = None
    GYD: Optional[float] = None
    HKD: Optional[float] = None
    HNL: Optional[float] = None
    HRK: Optional[float] = None
    HTG: Optional[float] = None
    HUF: Optional[float] = None
    IDR: Optional[float] = None
    ILS: Optional[float] = None
    IMP: Optional[float] = None
    INR: Optional[float] = None
    IQD: Optional[float] = None
    IRR: Optional[float] = None
    ISK: Optional[float] = None
    JEP: Optional[float] = None
    JMD: Optional[float] = None
    JOD: Optional[float] = None
    JPY: Optional[float] = None
    KES: Optional[float] = None
    KGS: Optional[float] = None
    KHR: Optional[float] = None
    KMF: Optional[float] = None
    KPW: Optional[float] = None
    KRW: Optional[float] = None
    KWD: Optional[float] = None
    KYD: Optional[float] = None
    KZT: Optional[float] = None
    LAK: Optional[float] = None
    LBP: Optional[float] = None
    LKR: Optional[float] = None
    LRD: Optional[float] = None
    LSL: Optional[float] = None
    LTL: Optional[float] = None
    LVL: Optional[float] = None
    LYD: Optional[float] = None
    MAD: Optional[float] = None
    MDL: Optional[float] = None
    MGA: Optional[float] = None
    MKD: Optional[float] = None
    MMK: Optional[float] = None
    MNT: Optional[float] = None
    MOP: Optional[float] = None
    MRU: Optional[float] = None
    MUR: Optional[float] = None
    MVR: Optional[float] = None
    MWK: Optional[float] = None
    MXN: Optional[float] = None
    MYR: Optional[float] = None
    MZN: Optional[float] = None
    NAD: Optional[float] = None
    NGN: Optional[float] = None
    NIO: Optional[float] = None
    NOK: Optional[float] = None
    NPR: Optional[float] = None
    NZD: Optional[float] = None
    OMR: Optional[float] = None
    PAB: Optional[float] = None
    PEN: Optional[float] = None
    PGK: Optional[float] = None
    PHP: Optional[float] = None
    PKR: Optional[float] = None
    PLN: Optional[float] = None
    PYG: Optional[float] = None
    QAR: Optional[float] = None
    RON: Optional[float] = None
    RSD: Optional[float] = None
    RUB: Optional[float] = None
    RWF: Optional[float] = None
    SAR: Optional[float] = None
    SBD: Optional[float] = None
    SCR: Optional[float] = None
    SDG: Optional[float] = None
    SEK: Optional[float] = None
    SGD: Optional[float] = None
    SHP: Optional[float] = None
    SLE: Optional[float] = None
    SLL: Optional[float] = None
    SOS: Optional[float] = None
    SRD: Optional[float] = None
    STD: Optional[float] = None
    SVC: Optional[float] = None
    SYP: Optional[float] = None
    SZL: Optional[float] = None
    THB: Optional[float] = None
    TJS: Optional[float] = None
    TMT: Optional[float] = None
    TND: Optional[float] = None
    TOP: Optional[float] = None
    TRY: Optional[float] = None
    TTD: Optional[float] = None
    TWD: Optional[float] = None
    TZS: Optional[float] = None
    UAH: Optional[float] = None
    UGX: Optional[float] = None
    USD: Optional[float] = None
    UYU: Optional[float] = None
    UZS: Optional[float] = None
    VEF: Optional[float] = None
    VES: Optional[float] = None
    VND: Optional[float] = None
    VUV: Optional[float] = None
    WST: Optional[float] = None
    XAF: Optional[float] = None
    XAG: Optional[float] = None
    XAU: Optional[float] = None
    XCD: Optional[float] = None
    XDR: Optional[float] = None
    XOF: Optional[float] = None
    XPF: Optional[float] = None
    YER: Optional[float] = None
    ZAR: Optional[float] = None
    ZMK: Optional[float] = None
    ZMW: Optional[float] = None
    ZWL: Optional[float] = None


class ExchangeRateResponse(BaseModel):
    base: str
    date: str
    rates: Rates
    success: bool
    timestamp: int


def parse_latest_response(response: Response) -> ExchangeRateResponse:
    """
    Parse the JSON content of the response and return it as a Pydantic model.

    :param response: The Response object from the requests library.
    :return: A Pydantic model matching the structure of the ExchangeRateResponse.
    """
    return ExchangeRateResponse(**response.json())


def validate_currency_key(currency: str) -> bool:
    return currency in Rates.model_fields


def get_latest(base_currency: str = "EUR", symbols: Optional[str] = "BRL,USD,EUR,JPY") -> Optional[Response]:
    """
    Fetch the latest exchange rates for the specified base currency and symbols.

    :param base_currency: The base currency for the exchange rates.
    :param symbols: A comma-separated list of currency symbols to retrieve rates for.
    :return: A Response object if the request is successful, otherwise None.
    """
    # validate base_currency against the list of supported currencies
    if not validate_currency_key(base_currency):
        raise BadRequest(f"Invalid base currency: {base_currency}")

    # validate symbols against the list of supported currencies
    if symbols:
        for symbol in symbols.split(","):
            if not validate_currency_key(symbol):
                raise BadRequest(f"Invalid symbol currency: {symbol}")

    response = requests.get(
        f"{EXCHANGE_BASE_URL}/latest", params={"base": base_currency, "symbols": symbols}, headers=HEADERS
    )
    response.raise_for_status()  # Raise an error for bad status codes
    return response
