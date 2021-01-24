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

    def test_create_new_url_collection_str(self):
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

    def test_create_new_url_item_str(self):
        """Test creating a new urlitem"""
        urlitem = models.URLItem.objects.create(
            title='Tryit Editor v3.6',
            url='https://www.w3schools.com/html/tryit.asp?'
                'filename=tryhtml_intro',
            visits=1,
            user=sample_user()
        )
        self.assertEqual(str(urlitem), urlitem.title)

    def test_assign_urlitems_to_urlcollection(self):
        """Test creating collections of urlitems"""
        user = sample_user()

        urlcollection = models.URLCollection.objects.create(
            name='Interesting HTML URLs',
            description='A collection of very interesting HTML test URLs',
            collection_type=models.URLCollection.OTHER,
            user=user
        )

        urlitem1 = models.URLItem.objects.create(
            title='Tryit Editor v3.6',
            url='https://www.w3schools.com/html/tryit.asp?'
                'filename=tryhtml_intro',
            visits=1,
            user=user
        )

        urlitem2 = models.URLItem.objects.create(
            title='HTML5test - How well does your browser support HTML5?',
            url='https://html5test.com',
            visits=1,
            user=user
        )

        models.URLCollectionItems.objects.create(
            collection=urlcollection,
            item=urlitem1,
            user=user
        )

        models.URLCollectionItems.objects.create(
            collection=urlcollection,
            item=urlitem2,
            user=user
        )

        urlcollection.refresh_from_db()

        self.assertEqual(urlcollection.items.all().count(), 2)
