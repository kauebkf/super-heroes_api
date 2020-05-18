from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


USERS_URL = reverse('user:user-list')

def user_profile_url(user_id):
    """Generates url for user profile"""
    return reverse('user:user-detail', args=[user_id])


class UserTests(TestCase):
    """Tests implementing a custom user model"""

    def test_create_user(self):
        """Tests creating an user and saving fields"""
        email = 'test@test.com'
        password = 'test'
        name = 'August'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
            name = name
        )
        self.assertEqual(user.email , email)
        self.assertEqual(user.name , name)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        """Test if creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        """Tests creating a superuser successfully"""
        user = get_user_model().objects.create_superuser(
            'test@superuser.com', 'pass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class AuthenticatedUserTests(TestCase):
    """Tests functions with authentication"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email = 'test@123.com',
            password = 'lasagna',
            name = 'Robins'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_users_list(self):
        """Testing listing users on users page"""
        res = self.client.get(USERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_modify_own_profile(self):
        """Tests modifying the user own profile"""
        res = self.client.patch(user_profile_url(self.user.id), name = 'Ivo Holanda')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_modify_profile_not_owned(self):
        """Tests modifying a profile other than the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email = 'other@example.com',
            password = 'haha',
            name = 'His name'
        )

        res = self.client.patch(user_profile_url(user2.id), name = 'math')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
