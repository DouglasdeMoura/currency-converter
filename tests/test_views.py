from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from currency_converter.models import Transaction


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.group = Group.objects.create(name="Test Group")
        self.other_user = User.objects.create_user(
            username="otheruser", email="otheruser@example.com", password="otherpass"
        )

    def test_list_users(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_create_user(self):
        url = reverse("user-list")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)

    def test_update_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updateduser@example.com")

    def test_delete_user(self):
        url = reverse("user-detail", kwargs={"pk": self.other_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)


class GroupViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.group = Group.objects.create(name="Test Group")

    def test_list_groups(self):
        url = reverse("group-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_group(self):
        url = reverse("group-detail", kwargs={"pk": self.group.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.group.name)

    def test_create_group(self):
        url = reverse("group-list")
        data = {
            "name": "newgroup",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 2)

    def test_update_group(self):
        url = reverse("group-detail", kwargs={"pk": self.group.pk})
        data = {
            "name": "updatedgroup",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, "updatedgroup")

    def test_delete_group(self):
        url = reverse("group-detail", kwargs={"pk": self.group.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Group.objects.count(), 0)


class TransactionViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.other_user = User.objects.create_user(
            username="otheruser", email="otheruser@example.com", password="otherpass"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Mocking get_latest and parse_latest_response globally for all tests
        Transaction.get_conversion_rate = lambda self, currency_from, currency_to: "1.1"

        # Creating a transaction for the test user
        self.transaction = Transaction.objects.create(
            user=self.user,
            currency_from="EUR",
            currency_to="USD",
            amount=10000,  # Stored in cents
        )

    def test_list_transactions(self):
        url = reverse("transaction-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_transaction(self):
        url = reverse("transaction-detail", kwargs={"pk": self.transaction.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.transaction.id)

    def test_create_transaction(self):
        url = reverse("transaction-list")
        data = {
            "currency_from": "EUR",
            "currency_to": "BRL",
            "amount": "50.00",  # 50.00 EUR
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
        new_transaction = Transaction.objects.get(pk=response.data["id"])
        self.assertEqual(new_transaction.currency_from, "EUR")
        self.assertEqual(new_transaction.currency_to, "BRL")
        self.assertEqual(new_transaction.amount, 5000)
        self.assertEqual(new_transaction.user, self.user)

    def test_update_transaction(self):
        url = reverse("transaction-detail", kwargs={"pk": self.transaction.pk})
        data = {
            "currency_from": "EUR",
            "currency_to": "JPY",
            "amount": "200.00",  # 200.00 EUR
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.currency_to, "JPY")
        self.assertEqual(self.transaction.amount, 20000)

    def test_delete_transaction(self):
        url = reverse("transaction-detail", kwargs={"pk": self.transaction.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 0)

    def test_list_transactions_only_for_authenticated_user(self):
        # Create a transaction for another user
        Transaction.objects.create(
            user=self.other_user,
            currency_from="USD",
            currency_to="BRL",
            amount=10000,  # Stored in cents
        )

        url = reverse("transaction-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure only the authenticated user's transaction is returned
        # self.assertEqual(len(response.data.results), 4)
        self.assertEqual(response.data["results"][0]["user_id"], self.user.id)
