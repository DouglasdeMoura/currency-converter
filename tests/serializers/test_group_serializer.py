from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory

from currency_converter.serializers import GroupSerializer


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
