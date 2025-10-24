from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.serializers import UserSerializer

User = get_user_model()


class UserModelTests(APITestCase):
    def test_create_user(self):
        username = "testuser123"
        password = "password1"
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class UserSerializerTests(APITestCase):
    def test_create_user_valid_data(self):
        payload = {
            "username": "testuser1",
            "password": "password123",
        }
        serializer = UserSerializer(data=payload)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.username, payload["username"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_password_too_short(self):
        payload = {
            "username": "testuser1",
            "password": "123",
        }
        serializer = UserSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class CreateUserTests(APITestCase):
    def setUp(self):
        self.create_url = reverse("user:create")

    def test_create_user_success(self):
        payload = {
            "username": "testuser1",
            "password": "testpass123",
        }

        res = self.client.post(self.create_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=payload["username"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_user_exists(self):
        payload = {
            "username": "testuser1",
            "password": "testpass123",
        }
        User.objects.create_user(**payload)

        res = self.client.post(self.create_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            "username": "testuser1",
            "password": "pw",
        }

        res = self.client.post(self.create_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            User.objects.filter(username=payload["username"]).exists()
        )
