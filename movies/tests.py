from django.test import TestCase

from movies.models import Comment, Movie


class TestMovieModel(TestCase):
    """
    Test class for Movies model.
    """

    def setUp(self):
        self.movie = Movie.objects.create(title='Terminator', year=1995, pk=1)

    def test_should_return_movie_object(self):
        """Test should return movie object."""
        self.assertTrue(isinstance(self.movie, Movie))
        self.assertTrue(hasattr(self.movie, 'title'))
        self.assertTrue(hasattr(self.movie, 'year'))

    def test_should_return__repr__movie_object(self):
        """Test should return repr object."""
        self.assertEqual(self.movie.__repr__(), self.movie.title)

    def test_should_return__str__movie_object(self):
        """Test should return string object."""
        self.assertEqual(self.movie.__str__(), '%s - %s' % (self.movie.title, self.movie.year))


class TestCommentModel(TestCase):
    """
    Test class for Comment model.
    """

    def setUp(self):
        self.movie = Movie.objects.create(title='Terminator', year=1995, pk=1)
        self.comment = Comment.objects.create(movie=self.movie, message='Testowy komentarz', pk=1)

    def test_should_return_comment_object(self):
        """Test should return comment object."""
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(self.comment.message, 'Testowy komentarz')
        self.assertEqual(self.comment.pk, 1)
        self.assertEqual(self.comment.movie_id, self.movie.pk)

    def test_should_return__repr__comment_object(self):
        """Test should return repr object."""
        self.assertEqual(self.comment.__repr__(), '%s: %s' % (self.movie.title, self.comment.message))

    def test_should_return__str__comment_object(self):
        """Test should return str object."""
        self.assertEqual(self.comment.__str__(), '%s: %s' % (self.comment.pk, self.comment.message))
