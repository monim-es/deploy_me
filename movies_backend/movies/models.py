from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    movie_id = models.IntegerField()  # TMDb movie ID
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie_id')  # prevent duplicates
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
