from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from heroes.serializers import HeroSerializer, HeroDetailSerializer
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

def marvel_hero_url(hero_id):
    return reverse('hero:marvel-detail', args=[hero_id])

def dc_hero_url(hero_id):
    return reverse('hero:dc-detail', args=[hero_id])

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


class AuthenticatedTests(TestCase):
    """Tests authenticated requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email = 'heroes@fan.com',
            password = 'nostalgia',
            name = 'Brian'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_dc_hero_from_marvel(self):
        """Tests retrieving dc hero from marvel url"""
        flash = create_sample_hero(
            alias = 'Flash',
            alter_ego = 'Barry Allen',
            universe = 'DC'
        )
        res = self.client.get(marvel_hero_url(flash.id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_marvel_hero_from_dc(self):
        """Tests retrieving marvel hero from dc url"""
        hulk = create_sample_hero()
        res = self.client.get(dc_hero_url(hulk.id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_not_owned_hero_marvel(self):
        """Tests retrieving a hero that you dont own"""
        hulk = create_sample_hero()

        res = self.client.get(marvel_hero_url(hulk.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_owned_hero_marvel(self):
        """Tests retrieving an owned hero"""
        hulk = create_sample_hero()
        self.user.superheroes.add(hulk)

        res = self.client.get(marvel_hero_url(hulk.id))
        serializer = HeroDetailSerializer(hulk)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_retrieve_not_owned_hero_dc(self):
        """Tests retrieving a hero that you dont own"""
        flash = create_sample_hero(
            alias = 'Flash',
            alter_ego = 'Barry Allen',
            universe = 'DC'
        )

        res = self.client.get(dc_hero_url(flash.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_owned_hero_dc(self):
        """Tests retrieving an owned hero"""
        flash = create_sample_hero(
            alias = 'Flash',
            alter_ego = 'Barry Allen',
            universe = 'DC'
        )
        self.user.superheroes.add(flash)

        res = self.client.get(dc_hero_url(flash.id))
        serializer = HeroDetailSerializer(flash)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
