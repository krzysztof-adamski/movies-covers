from django.db import models


class Movie(models.Model):
    """
    Stores a single movie
    :model:`movies.Movie`
    """
    title = models.CharField(
        max_length=255, unique=True, help_text="Movie title")
    year = models.IntegerField(
        null=True, blank=True, help_text="Movie year production")
    description = models.TextField(
        null=True, blank=True, help_text="Movie plot")

    def __str__(self):
        return "{} - {}".format(self.title, self.year)

    def __repr__(self):
        return "{}".format(self.title)


class Comment(models.Model):
    """
    Stores a comments related with one movie
    :model:`movies.Comment`
    movie_id: id of commented movie
    message: string content of the comment
    """
    movie = models.ForeignKey(Movie, related_name='comments',
                              on_delete=models.CASCADE, help_text="Related movie")
    message = models.CharField(max_length=255, help_text="Comment of movie")

    class Meta:
        #  unique_together = ('movie', 'message')
        ordering = ['movie']

    def __repr__(self):
        return '{}: {}'.format(self.movie.title, self.message)

    def __str__(self):
        return '{}: {}'.format(self.id, self.message)
