from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory

from currency_converter import models
from currency_converter.serializers import GroupSerializer, TransactionSerializer, UserSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.group = Group.objects.create(name="Test Group")
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.user.groups.add(self.group)
        self.client = APIClient()

    def test_user_serializer_fields(self):
        request = self.factory.get("/")
        serializer = UserSerializer(instance=self.user, context={"request": request})
        data = serializer.data
        self.assertEqual(set(data.keys()), set(["url", "username", "email", "groups"]))
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["email"], self.user.email)

    def test_user_serializer_invalid_data(self):
        invalid_data = {
            "username": "",
            "email": "not-an-email",
            "groups": [],
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)


class GroupSerializerTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.group = Group.objects.create(name="Test Group")
        self.client = APIClient()

    def test_group_serializer_fields(self):
        request = self.factory.get("/")
        serializer = GroupSerializer(instance=self.group, context={"request": request})
        data = serializer.data
        self.assertEqual(set(data.keys()), set(["url", "name"]))
        self.assertEqual(data["name"], self.group.name)

    def test_group_serializer_invalid_data(self):
        invalid_data = {
            "name": "",
        }
        serializer = GroupSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class TransactionSerializerTestCase(TestCase):
    def setUp(self):
        # Mocking get_conversion_rate before any transaction is saved
        models.Transaction.get_conversion_rate = lambda *args, **kwargs: "1.1"

        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.transaction_data = {
            "currency_from": "USD",
            "currency_to": "EUR",
            "amount": "100.00",
        }
        self.transaction = models.Transaction.objects.create(
            user=self.user,
            currency_from="USD",
            currency_to="EUR",
            amount=10000,  # Stored in cents
        )

    def test_transaction_serializer_valid_data(self):
        serializer = TransactionSerializer(data=self.transaction_data, context={"request": None})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["amount"], 10000)  # Amount should be in cents

    def test_transaction_serializer_create(self):
        serializer = TransactionSerializer(data=self.transaction_data, context={"request": None})
        serializer.is_valid()
        transaction = serializer.save(user=self.user)  # Pass the user explicitly when saving
        self.assertEqual(transaction.amount, 10000)  # Stored in cents
        self.assertEqual(transaction.user, self.user)

    def test_transaction_serializer_to_representation(self):
        serializer = TransactionSerializer(instance=self.transaction, context={"request": None})
        data = serializer.data
        self.assertEqual(data["amount"], Decimal("100.00"))  # Converted back to dollars
        self.assertEqual(data["converted_amount"], Decimal("110.00"))  # Converted back to dollars
        self.assertEqual(data["currency_from"], "USD")
        self.assertEqual(data["currency_to"], "EUR")
        self.assertEqual(data["user_id"], self.user.id)

    def test_transaction_serializer_read_only_fields(self):
        update_data = {
            "id": 999,
            "user": User.objects.create_user(
                username="otheruser", email="otheruser@example.com", password="otherpass"
            ).id,
            "conversion_rate": 2.0,
            "converted_amount": 20000,
            "timestamp": "2025-01-01T00:00:00Z",
            "currency_from": "USD",
            "currency_to": "GBP",
            "amount": "50.00",
        }
        serializer = TransactionSerializer(instance=self.transaction, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_transaction = serializer.save()

        # The read-only fields should not have been updated
        self.assertNotEqual(updated_transaction.id, update_data["id"])
        self.assertNotEqual(updated_transaction.user, update_data["user"])
        self.assertNotEqual(updated_transaction.conversion_rate, update_data["conversion_rate"])
        self.assertNotEqual(updated_transaction.converted_amount, update_data["converted_amount"])
        self.assertNotEqual(updated_transaction.timestamp, update_data["timestamp"])

    def test_transaction_serializer_invalid_amount(self):
        invalid_data = self.transaction_data.copy()
        invalid_data["amount"] = "invalid_amount"  # Non-numeric value for amount
        serializer = TransactionSerializer(data=invalid_data, context={"request": None})
        self.assertFalse(serializer.is_valid())
        self.assertIn("amount", serializer.errors)
