from django.test import TestCase

from movies.serializers import TopRankMovieSerializer
from movies.models import Comment, Movie


class TestTopRankMovieSerializer(TestCase):

    def setUp(self):

        self.movie_data = {
            'pk': 1,
            'title': 'Movie',
            'year': 2015,
            'description': ''
        }
        self.movie_data2 = {
            'pk': 2,
            'title': 'Movie2',
            'year': 2019,
            'description': ''
        }

        self.movie = Movie.objects.create(**self.movie_data)
        Comment.objects.create(movie=self.movie, message='Testowy komentarz 1')
        Comment.objects.create(movie=self.movie, message='Testowy komentarz 2')
        Comment.objects.create(movie=self.movie, message='Testowy komentarz 3')
        Comment.objects.create(movie=self.movie, message='Testowy komentarz 4')

        self.movie2 = Movie.objects.create(**self.movie_data2)
        Comment.objects.create(movie=self.movie2, message='Testowy komentarz 1')
        Comment.objects.create(movie=self.movie2, message='Testowy komentarz 2')

        self.data = [
            {
                'total_comments': 4,
                'movie_id': 1,
                'year': 2015,
                'rank': 1,
            },
            {
                'total_comments': 2,
                'movie_id': 1,
                'year': 2019,
                'rank': 2
            }
        ]
        self.serializer = TopRankMovieSerializer(instance=self.data, many=True)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data[0].keys()), set(['total_comments', 'movie_id', 'rank', 'year']))
        self.assertEqual(len(set(data[0].keys())), 4)

    def test_rank_field_in_content(self):
        data = self.serializer.data
        self.assertEqual(self.data[0]['rank'], data[0]['rank'])

    def test_raise_serializer_exception(self):
        self.data[0]['total_comments'] = 'abc'
        self.serializer = TopRankMovieSerializer(instance=self.data, many=True)
        with self.assertRaises(ValueError) as context:
            self.serializer.data
        self.assertTrue("invalid literal for int() with base 10: 'abc'" in context.exception.args[0])
