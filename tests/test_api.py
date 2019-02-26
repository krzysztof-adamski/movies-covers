from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


API_OMD_CONFIG = {
    'API_KEY': 'sdsds',
    'API_URL': 'http://www.omdbapi.com/'
}


@patch('movies.providers.API_OMD_CONFIG', API_OMD_CONFIG)
class MovieAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_empty_movie_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])
