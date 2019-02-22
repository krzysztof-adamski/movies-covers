from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from movies.models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        max_length=255,
        validators=[
            UniqueValidator(queryset=Movie.objects.all())
        ]
    )
    year = serializers.IntegerField(
        min_value=1,
        style={'input_type': 'hidden'},
        label=''
    )
    description = serializers.CharField(
        style={'input_type': 'hidden'},
        label=''
    )

    class Meta:
        model = Movie
        fields = ('title', 'id', 'year', 'description')


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    message = serializers.CharField(
        style={'base_template': 'textarea.html', 'rows': 3},
        label='Comment'
    )

    class Meta:
        model = Comment
        fields = ('id', 'movie', 'message')


class TopRankMovieSerializer(serializers.ModelSerializer):
    total_comments = serializers.IntegerField()
    movie_id = serializers.IntegerField()
    year = serializers.IntegerField()
    rank = serializers.IntegerField()

    class Meta:
        fields = ('movie_id', 'total_comments', 'rank', 'year')
        model = Movie
