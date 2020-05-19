from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from heroes.serializers import HeroSerializer


HEROES_URL = reverse('hero:hero-list')

class PublicTests(TestCase):
    """Tests unauthenticated access"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_hero(self):
        """Unauthenticated users can see the heroes"""
        res = self.client.get(HEROES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
