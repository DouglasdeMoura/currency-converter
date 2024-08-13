from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


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
