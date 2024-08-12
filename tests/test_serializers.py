from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory

from currency_converter.serializers import GroupSerializer, UserSerializer


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
