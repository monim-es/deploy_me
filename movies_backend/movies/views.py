from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .utils.tmdb import get_trending_movies, get_movie_details
import requests
from django.conf import settings
from rest_framework import generics, permissions
from .models import FavoriteMovie
from .serializers import FavoriteMovieSerializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


class TrendingMoviesView(APIView):
    def get(self, request):
        print("⚡ Fetching trending movies from TMDb API")
        movies = get_trending_movies()
        return Response(movies)


class TMDbRecommendationsView(APIView):
    def get(self, request, movie_id):
        print(f"⚡ Fetching recommendations from TMDb for movie {movie_id}")
        api_key = settings.TMDB_API_KEY
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
        params = {"api_key": api_key, "language": "en-US", "page": 1}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json().get("results", [])
            return Response(data)
        else:
            return Response({"error": "Failed to fetch recommendations."}, status=500)


class MovieDetailView(APIView):
    def get(self, request, movie_id):
        try:
            movie = get_movie_details(movie_id)
            return Response(movie)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class FavoriteMovieListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteMovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"detail": "Movie already in favorites."})


class FavoriteMovieDeleteView(generics.DestroyAPIView):
    serializer_class = FavoriteMovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Movie removed from favorites."}, status=status.HTTP_200_OK)













# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .utils.tmdb import get_trending_movies, get_movie_details
# import requests
# from django.conf import settings
# from rest_framework import generics, permissions
# from .models import FavoriteMovie
# from .serializers import FavoriteMovieSerializer
# from django.db import IntegrityError
# from rest_framework.exceptions import ValidationError
# from django.core.cache import cache  # Redis cache



# # this class doesn't use caching 
# # class TrendingMoviesView(APIView):
# #     def get(self, request):
# #         movies = get_trending_movies()
# #         return Response(movies)



# # class TMDbRecommendationsView(APIView):
# #     def get(self, request, movie_id):
# #         api_key = settings.TMDB_API_KEY
# #         url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
# #         params = {
# #             "api_key": api_key,
# #             "language": "en-US",
# #             "page": 1,
# #         }

# #         response = requests.get(url, params=params)

# #         if response.status_code == 200:
# #             data = response.json()
# #             if data["results"]:
# #                 return Response(data["results"], status=200)
# #             else:
# #                 return Response({"message": "No recommendations found for this movie."}, status=200)
# #         else:
# #             return Response({"error": "Failed to fetch recommendations from TMDb."}, status=500)






# ################################################# movie details & handling favorite movies #########################""
# class MovieDetailView(APIView):
#     def get(self, request, movie_id):
#         try:
#             movie = get_movie_details(movie_id)
#             return Response(movie)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

# #handling favorites movies 



# class FavoriteMovieListCreateView(generics.ListCreateAPIView):
#     serializer_class = FavoriteMovieSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return FavoriteMovie.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         try:
#             serializer.save(user=self.request.user)
#         except IntegrityError:
#             raise ValidationError({"detail": "Movie already in favorites."})
    

# class FavoriteMovieDeleteView(generics.DestroyAPIView):
#     serializer_class = FavoriteMovieSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return FavoriteMovie.objects.filter(user=self.request.user)

#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response({"message": "Movie removed from favorites."}, status=status.HTTP_200_OK)
    
# ########################################"" new one for cashing  ####################################################
# class TrendingMoviesView(APIView):
#     def get(self, request):
#         cache_key = "trending_movies"
#         cached_data = cache.get(cache_key)

#         if cached_data:
#             print("🔁 Using cached trending movies")
#             return Response(cached_data)

#         print("⚡ Fetching trending movies from TMDb API")
#         movies = get_trending_movies()
#         cache.set(cache_key, movies, timeout=60 * 60)  # Cache for 1 hour
#         return Response(movies)


# class TMDbRecommendationsView(APIView):
#     def get(self, request, movie_id):
#         cache_key = f"recommendations_movie_{movie_id}"
#         cached_data = cache.get(cache_key)

#         if cached_data:
#             print(f"🔁 Using cached recommendations for movie {movie_id}")
#             return Response(cached_data)

#         print(f"⚡ Fetching recommendations from TMDb for movie {movie_id}")
#         api_key = settings.TMDB_API_KEY
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
#         params = {"api_key": api_key, "language": "en-US", "page": 1}

#         response = requests.get(url, params=params)

#         if response.status_code == 200:
#             data = response.json().get("results", [])
#             cache.set(cache_key, data, timeout=60 * 60)
#             return Response(data)
#         else:
#             return Response({"error": "Failed to fetch recommendations."}, status=500)
