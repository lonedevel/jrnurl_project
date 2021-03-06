from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import URLCollection, URLItem
from jrnurl.serializers import URLCollectionSerializer, URLItemSerializer

URLCOLLECTION_URL = reverse('jrnurl:urlcollection-list')
URLITEM_URL = reverse('jrnurl:urlitem-list')


class PublicApiTests(TestCase):
    """Tests the public APIs for jrnurlapp"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(URLCOLLECTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
    """Tests the private APIS for jrnurlapp"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testuser@testdomain.com',
            'test1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_urlcollection_list(self):
        """Test retrieving a list of urlcollections"""
        URLCollection.objects.create(
            name='Interesting HTML URLs',
            description='A collection of very interesting HTML test URLs',
            collection_type=URLCollection.OTHER,
            user=self.user
        )

        URLCollection.objects.create(
            name='Other HTML URLs',
            description='A collection of other interesting HTML test URLs',
            collection_type=URLCollection.OTHER,
            user=self.user
        )

        res = self.client.get(URLCOLLECTION_URL)
        urlcollections = URLCollection.objects.filter(user=self.user)
        serializer = URLCollectionSerializer(urlcollections, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_urlitem_list(self):
        """Test retrieving a list of urlitems"""
        URLItem.objects.create(
            title='Tryit Editor v3.6',
            url='https://www.w3schools.com/html/tryit.asp?'
                'filename=tryhtml_intro',
            visits=1,
            user=self.user
        )

        URLItem.objects.create(
            title='HTML5test - How well does your browser support HTML5?',
            url='https://html5test.com',
            visits=1,
            user=self.user
        )

        res = self.client.get(URLITEM_URL)
        urlitems = URLItem.objects.filter(user=self.user)
        serializer = URLItemSerializer(urlitems, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_complex_urlcollection(self):
        """Test retrieving a complex urlcollection
        with assigned urlitems and keywords"""
        urlcollection = URLCollection.objects.create(
            name='Interesting HTML URLs',
            description='A collection of very interesting HTML test URLs',
            collection_type=URLCollection.OTHER,
            user=self.user
        )
        urlcollection.save()

        urlitem1 = URLItem.objects.create(
            title='Tryit Editor v3.6',
            url='https://www.w3schools.com/html/tryit.asp?'
                'filename=tryhtml_intro',
            visits=1,
            user=self.user
        )
        urlitem1.save()

        urlitem2 = URLItem.objects.create(
            title='HTML5test - How well does your browser support HTML5?',
            url='https://html5test.com',
            visits=1,
            user=self.user
        )
        urlitem2.save()

        urlcollection.items.add(urlitem1, through_defaults={'user': self.user})
        urlcollection.items.add(urlitem2, through_defaults={'user': self.user})
        urlcollection.keywords = ['html', 'web', 'browser']

        res = self.client.get(URLCOLLECTION_URL)
        urlcollections = URLCollection.objects.filter(user=self.user)
        serializer = URLCollectionSerializer(urlcollections, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_simple_urlcollection_successful(self):
        """Test creating a new simple urlcollection
        using the api is successful"""
        payload = {
            'name': 'Simple URL Collection',
            'description':
                'A nicely curated test collection of incredible URLs',
            'collection_type': 400,
            'user': self.user.id
        }
        res = self.client.post(URLCOLLECTION_URL, payload)
        # print(res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = URLCollection.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_simple_urlcollection_unsuccessful(self):
        """Test creating a new simple urlcollection
        using the api is unsuccessful"""
        payload = {
            'name': 'Simple URL Collection',
            'description':
                'A nicely curated test collection of incredible URLs',
            'collection_type': 400
        }
        res = self.client.post(URLCOLLECTION_URL, payload)
        # print(res.data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        exists = URLCollection.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertFalse(exists)

    def test_create_complex_urlcollection_successful(self):
        """Test creating a new complex urlcollection using the api"""
        payload = {
            'name': 'Complex URL Collection',
            'description':
                'A nicely curated test collection of incredible URLs',
            'collection_type': 400,
            'user': self.user.id,
            'keywords': ['test', 'url', 'complex'],
            'items': [
                {
                    'title':
                        'HTML5test - '
                        'How well does your browser support HTML5?',
                    'url': 'https://html5test.com',
                    'visits': 1,
                    'user': self.user.id
                },
                {
                    'title': 'Google Search',
                    'url': 'http://google.com',
                    'visits': 1,
                    'user': self.user.id
                }
            ]
        }
        res = self.client.post(URLCOLLECTION_URL, payload)
        # print(res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = URLCollection.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_urlitem_successful(self):
        """Test creating a new urlitem is successful"""
        payload = {
            'title': 'Google Search',
            'url': 'http://google.com',
            'visits': 1,
            'user': self.user.id
        }

        res = self.client.post(URLITEM_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = URLItem.objects.filter(
            user=self.user,
            title=payload['title']
        ).exists()
        self.assertTrue(exists)

    def test_create_urlitem_unsuccessful(self):
        """Test creating a urlitem is unsuccessful"""
        payload = {
            'title': 'Google Search',
            'url': 'http://google.com',
            'visits': 1
        }

        res = self.client.post(URLITEM_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        exists = URLItem.objects.filter(
            user=self.user,
            title=payload['title']
        ).exists()
        self.assertFalse(exists)

    def test_delete_urlcollection_successful(self):
        """Test deleting a urlcollection is successful"""
        urlcollection = URLCollection.objects.create(
            name='Interesting HTML URLs',
            description='A collection of very interesting HTML test URLs',
            collection_type=URLCollection.OTHER,
            user=self.user
        )
        urlcollection.save()

        delete_url = f'{URLCOLLECTION_URL}{urlcollection.id}/'
        res = self.client.delete(delete_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = URLCollection.objects.filter(
            user=self.user,
            id=urlcollection.id
        ).exists()
        self.assertFalse(exists)

    def test_delete_urlitem_successful(self):
        """Test deleting a urlitem is successful"""
        urlitem = URLItem.objects.create(
            title='Tryit Editor v3.6',
            url='https://www.w3schools.com/html/tryit.asp?'
                'filename=tryhtml_intro',
            visits=1,
            user=self.user
        )
        urlitem.save()

        delete_url = f'{URLITEM_URL}{urlitem.id}/'
        res = self.client.delete(delete_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = URLItem.objects.filter(
            user=self.user,
            id=urlitem.id
        ).exists()
        self.assertFalse(exists)

    def test_update_urlcollection_successful(self):
        """Test updating a URL Collection succesfully via a put request"""
        payload = {
            'name': 'Simple URL Collection',
            'description':
                'A nicely curated test collection of incredible URLs',
            'collection_type': 400,
            'user': self.user
        }
        urlcollection = URLCollection.objects.create(**payload)
        urlcollection.save()

        payload['description'] = 'The quick brown fox jumped over ' \
                                 'the lazy dog!'
        payload['user'] = self.user.id

        urlcollection_put_url = f'{URLCOLLECTION_URL}{urlcollection.id}/'

        res = self.client.put(urlcollection_put_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        compare_urlcollection = URLCollection.objects.get(
            user=self.user,
            id=urlcollection.id
        )

        self.assertEqual(compare_urlcollection.description,
                         payload['description'])

# TODO Add tests for updating URLItems
# TODO Add tests for updating complex URLCollections
# TODO Add test for creating large batch complex URLCollection
