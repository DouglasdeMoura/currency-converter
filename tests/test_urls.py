from django.test import SimpleTestCase
from django.urls import resolve, reverse

from currency_converter.views import GroupViewSet, TransactionViewSet, UserViewSet


class TestUrls(SimpleTestCase):
    def test_users_list_url_resolves(self):
        url = reverse("user-list")
        self.assertEqual(resolve(url).func.__name__, UserViewSet.as_view({"get": "list"}).__name__)

    def test_users_detail_url_resolves(self):
        url = reverse("user-detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.__name__, UserViewSet.as_view({"get": "retrieve"}).__name__)

    def test_groups_list_url_resolves(self):
        url = reverse("group-list")
        self.assertEqual(resolve(url).func.__name__, GroupViewSet.as_view({"get": "list"}).__name__)

    def test_groups_detail_url_resolves(self):
        url = reverse("group-detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.__name__, GroupViewSet.as_view({"get": "retrieve"}).__name__)

    def test_api_auth_login_url_resolves(self):
        url = reverse("rest_framework:login")
        self.assertEqual(resolve(url).url_name, "login")

    def test_api_auth_logout_url_resolves(self):
        url = reverse("rest_framework:logout")
        self.assertEqual(resolve(url).url_name, "logout")

    def test_transactions_list_url_resolves(self):
        url = reverse("transaction-list")
        self.assertEqual(resolve(url).func.__name__, TransactionViewSet.as_view({"get": "list"}).__name__)

    def test_transactions_detail_url_resolves(self):
        url = reverse("transaction-detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.__name__, TransactionViewSet.as_view({"get": "retrieve"}).__name__)
