"""URL configuration for the mental health app."""

from django.urls import path
from .mental_health_app_views import login_view, track_mood, mood_statistics  # Assuming .views is correct

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('track-mood/', track_mood, name='track_mood'),
    path('mood-statistics/', mood_statistics, name='mood_statistics'),
]
