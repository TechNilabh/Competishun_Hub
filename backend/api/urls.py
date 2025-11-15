from django.urls import path
from . import views

urlpatterns = [
    path("submit/", views.submit),
    path("leaderboard/", views.leaderboard),
    path("history/", views.history),
]
