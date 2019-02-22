from django_filters import FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from rest_framework import (
    filters,
    generics,
    status,
    viewsets,
    mixins
)
from rest_framework.response import Response

from movies.models import Comment, Movie
from movies.exceptions import (
    CommunicationError,
    ObjectDoesNotExist,
    ValidationError
)
from movies.providers import OmdbMoviesProvider
from movies.serializers import (
    CommentSerializer,
    MovieSerializer,
    TopRankMovieSerializer
)


class YearRangeFilter(FilterSet):
    since = NumberFilter(
        field_name='year', label='From year', lookup_expr='gte')
    to = NumberFilter(field_name='year', label='To year', lookup_expr='lte')

    class Meta:
        model = Movie
        fields = ['since', 'to']


class MoviesListView(generics.ListCreateAPIView):
    """
    Endpoint to create and list movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('title',)
    ordering_fields = ('year', 'title')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = OmdbMoviesProvider()

    def post(self, request, format=None):
        title = request.data.get('title')
        try:
            movie = self.provider.search_movie(title)
            serializer = MovieSerializer(data=movie)
        except AssertionError as exc:
            return Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as exc:
            return Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as exc:
            return Response(exc.args[0], status=status.HTTP_404_NOT_FOUND)
        except CommunicationError as exc:
            return Response(exc.args[0], status=status.HTTP_408_REQUEST_TIMEOUT)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentsListView(generics.ListAPIView):
    """
    Endpoint to posting or viewing comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('movie__id',)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopRankMoviesListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Endpoint to view top rank movies, filters by year
    """
    filter_class = YearRangeFilter
    serializer_class = TopRankMovieSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('min_year', 'max_year')
    queryset = Movie.objects.annotate(
        comment_count=Count('comments'),
    )
    search_fields = ('year',)

    def get_rank(self, data=[], comments=1):
        """Method to set rank the movie."""
        if not data:
            return 1
        try:
            if data[-1]['total_comments'] == comments:
                return data[-1]['rank']
            else:
                return data[-1]['rank'] + 1
        except KeyError as exc:
            return Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)
        if data[-1]['total_comments'] == comments:
            return data[-1]['rank']
        else:
            return data[-1]['rank'] + 1

    def list(self, request):
        queryset = self.get_queryset().order_by('-comment_count')
        f = YearRangeFilter(request.GET, queryset=queryset)
        data = []
        for movie in f.qs:
            data.extend([{
                'movie_id': movie.id,
                'total_comments': movie.comment_count,
                'rank': self.get_rank(data, movie.comment_count),
                'year': movie.year
            }])
        serializer = TopRankMovieSerializer(data, many=True)
        return Response(serializer.data)
