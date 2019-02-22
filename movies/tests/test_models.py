from django.test import TestCase
from movies.models import Movie


class TestMovieModel(TestCase):
    """
    Test class for Movies model test.
    """

    def setUp(self):
        Movie.objects.create(title='Terminator', year=1995)

    def test_should_return__repr__object(self):
        """Test should return string repr object."""
        obj = Movie.objects.get(title='Terminator')
        self.assertTrue(isinstance(obj, Movie))
        self.assertEqual(obj.__repr__(), 'Terminator')

    def test_should_return__str__object(self):
        """Test should return string repr object."""
        obj = Movie.objects.get(title='Terminator')
        self.assertTrue(isinstance(obj, Movie))
        self.assertEqual(obj.__str__(), 'Terminator - 1995')
