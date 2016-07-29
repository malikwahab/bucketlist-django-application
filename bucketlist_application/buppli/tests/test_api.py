from django.test import TestCase
from rest_framework import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class Testauthentication(APITestCase):

    def test_register(self):
        data = {"username": "malikwahab", "password": "malik"}
        url = "auth/register"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'malikwahab')
