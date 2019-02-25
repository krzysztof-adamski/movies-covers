from django.conf import settings

import requests
from requests.exceptions import ConnectionError, Timeout

from .exceptions import CommunicationError, ObjectDoesNotExist
from .schemas import OmdbMovieSchema


API_OMD_CONFIG = getattr(settings, 'API_OMD_CONFIG', {})


class OmdbMoviesProvider(object):
    """
    OmdbMoviesProvider is a class which delivers information about movies
    from external service.
    """

    def __init__(self):
        """
        OMDB service require api_key to use movie database.
        """
        self.api_key = API_OMD_CONFIG.get('API_KEY')
        self.api_url = API_OMD_CONFIG.get('API_URL')
        assert self.api_key and self.api_url, "No API_OMD_CONFIG in settings"

    def search_movie(self, title):
        """
        Function search movie in external source and return one of them.
        Returned data are serialized by schema.
        """
        assert title, "Title can't be empty"
        params = {'t': title, 'apikey': self.api_key, 'r': 'json'}
        try:
            response = requests.get(url=self.api_url, params=params)
        except (Timeout, ConnectionError) as exc:
            raise CommunicationError(exc.args[0])
        if response.json().get('Error') == 'Movie not found!':
            raise ObjectDoesNotExist(response.json())
        if response.ok:
            schema = OmdbMovieSchema()
            data = schema.load(response.json()).data
            return data
        elif response.status_code == 404:
            raise ObjectDoesNotExist(response.json())
        else:
            raise CommunicationError(response.json())
