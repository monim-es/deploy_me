import os
import requests


TMDB_API_KEY = "d52ee3f3c81fbdb1a02f46ebb8c7c81b"
BASE_URL = "https://api.themoviedb.org/3"

def get_trending_movies():
    url = f"{BASE_URL}/trending/movie/week"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("results", [])

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
