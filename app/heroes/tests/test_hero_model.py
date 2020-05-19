from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from heroes.serializers import HeroSerializer
from core import models


HEROES_URL = reverse('hero:hero-list')
MARVEL_URL = reverse('hero:marvel-list')
DC_URL = reverse('hero:dc-list')

def create_sample_hero(**params):
    """Creates a sample hero"""
    hero = {
        'alias': 'Hulk',
        'alter_ego': 'Bruce Banne',
        'universe': 'Marvel',
    }
    hero.update(params)

    return models.Hero.objects.create(**hero)

class PublicTests(TestCase):
    """Tests unauthenticated access"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_hero(self):
        """Unauthenticated users can see the heroes"""
        res = self.client.get(HEROES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_hero_not_allowed(self):
        payload = {
            'alias': 'Batman',
            'alter_ego': 'Bruce Wayne'
        }
        res = self.client.post(HEROES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_marvel_only(self):
        """Tests returning Marvel heroes only"""

        hulk = create_sample_hero()
        arrow = create_sample_hero(
            alias = 'Arrow',
            alter_ego = 'Oliver Queen',
            universe = 'DC'
        )

        res = self.client.get(MARVEL_URL)

        marvel_heroes = models.Hero.objects.filter(universe='Marvel')
        serializer = HeroSerializer(marvel_heroes, many=True)
        serializer2 = HeroSerializer(arrow)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_return_dc_only(self):
        """Tests returning DC heroes only"""
        diana = create_sample_hero(
            alias = 'Wonder Woman',
            alter_ego = 'Diana',
            universe = 'DC'
        )

        hulk = create_sample_hero()

        res = self.client.get(DC_URL)

        dc_heroes = models.Hero.objects.filter(universe='DC')
        serializer = HeroSerializer(dc_heroes, many=True)
        hulk_serialized = HeroSerializer(hulk)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
        self.assertNotIn(hulk_serialized.data, res.data)
