from django.db import models
from django.contrib.auth.models import User

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="submissions/")
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    best_score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.best_score}"
