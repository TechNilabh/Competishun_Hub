from django.contrib import admin
from .models import Submission, Leaderboard

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'timestamp')
    list_filter = ('user',)
    ordering = ('-score',)

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'best_score')
    ordering = ('-best_score',)
