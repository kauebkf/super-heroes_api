from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTests(TestCase):
    """Tests implementing a custom user model"""

    def test_create_user(self):
        """A simple test to create an user"""
        user = get_user_model().objects.create()
