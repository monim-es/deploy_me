from django.urls import path
from .views import TrendingMoviesView, MovieDetailView, TMDbRecommendationsView, FavoriteMovieListCreateView, FavoriteMovieDeleteView

urlpatterns = [
    path('trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('<int:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('recommendations/<int:movie_id>/', TMDbRecommendationsView.as_view(), name='movie_recommendations'),

    path('favorites/', FavoriteMovieListCreateView.as_view(), name='favorites-list-create'),
    path('favorites/<int:pk>/', FavoriteMovieDeleteView.as_view(), name='favorite-delete'),

]
