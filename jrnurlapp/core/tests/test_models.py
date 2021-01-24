from django.test import TestCase
# from unittest.mock import patch
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='testuser@emaildomain.com', password='test1234'):
    """ Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test database models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@emaildomain.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if the email for a new user is normalized"""
        email = 'test@EMAILDOMAIN.COM'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating a user without an email address raises error"""
        email = None
        password = 'Testpass123'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=email,
                password=password
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = 'test@emaildomain.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_new_url_collection(self):
        """Test creating a new urlcollection"""
        urlcollection = models.URLCollection.objects.create(
            name='Interesting URLs',
            description='A collection of very interesting URLs',
            collection_type=models.URLCollection.OTHER,
            user=sample_user()
        )
        self.assertEqual(str(urlcollection),
                         f'{urlcollection.get_collection_type_display()} - '
                         f'{urlcollection.name}')
