from decimal import Decimal

import structlog
from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import APIException

from currency_converter.services.exchanges_rates_data_api import get_latest, parse_latest_response


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_from = models.CharField(max_length=3)
    currency_to = models.CharField(max_length=3)
    amount = models.IntegerField()
    conversion_rate = models.CharField(editable=False, max_length=255)
    converted_amount = models.IntegerField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def save(self, *args, **kwargs):
        try:
            self.conversion_rate = self.get_conversion_rate(self.currency_from, self.currency_to)
            self.converted_amount = self.convert_amount(self.amount, self.conversion_rate)
            super().save(*args, **kwargs)
        except Exception as e:
            logger = structlog.get_logger(__name__)
            logger.error("An error occurred while saving the transaction:", error=e)
            raise APIException("An error occurred while saving the transaction")

    def get_conversion_rate(self, currency_from, currency_to) -> str:
        """Gets the conversion rate between two currencies

        Args:
            currency_from (str): The currency to convert from
            currency_to (str): The currency to convert to

        Returns:
            str: The conversion rate, as a string
        """
        if currency_from == currency_to:
            return "1"

        response = parse_latest_response(get_latest(currency_from, currency_to))
        # The conversion rate is stored as a string to avoid floating point arithmetic issues
        rate = str(response.rates.model_dump().get(currency_to))
        return rate

    def convert_amount(self, amount: int, rate: str) -> int:
        """Converts the amount to the currency_to currency

        Args:
            amount (int): The amount to convert
            rate (str): The exchange rate

        Returns:
            int: The converted amount, in cents
        """
        # The number of digits after the decimal point in the rate plus 3 (to account for rounding)
        splitted_number = rate.split(".")
        number_of_digits: int = len(splitted_number[1]) + 3 if len(splitted_number) > 1 else 3
        # The multiplier is used to avoid floating point arithmetic issues
        multiplier: int = 10**number_of_digits
        return round(((amount * multiplier) * int(Decimal(rate) * multiplier)) / multiplier**2)
