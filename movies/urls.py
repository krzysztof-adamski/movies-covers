from django.urls import path
from movies import views

urlpatterns = [
    path('movies/', views.MoviesListView.as_view(), name="movie-list"),
    path('comments/', views.CommentsListView.as_view(), name="comments-list"),
    path('top/', views.TopRankMoviesListViewSet.as_view({'get': 'list'}), name="rank-list"),
]
