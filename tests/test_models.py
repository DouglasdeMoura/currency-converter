from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from currency_converter.models import Transaction


class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")

    @patch("currency_converter.models.Transaction.get_conversion_rate")
    def test_save_transaction(self, mock_get_conversion_rate):
        mock_get_conversion_rate.return_value = "1.1"

        # Create a transaction
        transaction = Transaction(
            user=self.user,
            currency_from="EUR",
            currency_to="USD",
            amount=10000,  # 100.00 EUR in cents
        )
        transaction.save()

        # Test conversion rate and converted amount
        self.assertEqual(transaction.conversion_rate, "1.1")
        self.assertEqual(transaction.converted_amount, 11000)  # 100.00 EUR * 1.1 -> 110.00 USD (rounded to 11000 cents)

    def test_get_conversion_rate_same_currency(self):
        transaction = Transaction(
            user=self.user,
            currency_from="EUR",
            currency_to="EUR",
            amount=10000,  # 100.00 EUR in cents
        )
        rate = transaction.get_conversion_rate(transaction.currency_from, transaction.currency_to)
        self.assertEqual(rate, "1")

    @patch("currency_converter.models.Transaction.get_conversion_rate")
    def test_get_conversion_rate_different_currencies(self, mock_get_conversion_rate):
        # Mock the external API call and parsing logic
        mock_get_conversion_rate.return_value = "1.1"

        transaction = Transaction(
            user=self.user,
            currency_from="EUR",
            currency_to="USD",
            amount=10000,  # 100.00 EUR in cents
        )
        rate = transaction.get_conversion_rate(transaction.currency_from, transaction.currency_to)
        self.assertEqual(rate, "1.1")

    def test_convert_amount(self):
        transaction = Transaction(
            user=self.user,
            currency_from="EUR",
            currency_to="USD",
            amount=10000,  # 100.00 EUR in cents
        )
        rate = "1.1"
        converted_amount = transaction.convert_amount(transaction.amount, rate)
        self.assertEqual(converted_amount, 11000)  # 100.00 EUR * 1.1 -> 110.00 USD (rounded to 11000 cents)

    @patch("currency_converter.models.Transaction.get_conversion_rate")
    def test_full_transaction_creation(self, mock_get_conversion_rate):
        # Mock the external API call and parsing logic
        mock_get_conversion_rate.return_value = "1.1"

        # Save a new transaction and check fields
        transaction = Transaction(
            user=self.user,
            currency_from="EUR",
            currency_to="USD",
            amount=10000,  # 100.00 EUR in cents
        )
        transaction.save()

        self.assertEqual(transaction.conversion_rate, "1.1")
        self.assertEqual(transaction.converted_amount, 11000)  # 110.00 USD -> 11000 cents
        self.assertIsNotNone(transaction.timestamp)
