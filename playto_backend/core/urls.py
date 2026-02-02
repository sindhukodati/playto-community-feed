from django.urls import path
from .views import (
    FeedView,
    LeaderboardView,
    CreatePostView,
)

urlpatterns = [
    path("feed/", FeedView.as_view()),
    path("posts/", CreatePostView.as_view()),   # 👈 POST API
    path("leaderboard/", LeaderboardView.as_view()),
]
