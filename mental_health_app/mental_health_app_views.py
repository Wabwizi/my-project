"""
This module contains the views for user authentication, mood tracking,
and mood statistics for the mental health app.
"""

from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import MoodEntry


# Login view (with redirect to mood statistics after login)
def login_view(request):
    """
    Handles user login. Authenticates the user and redirects to mood statistics after successful login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to mood statistics after login
                return redirect('mood_statistics')
            else:
                # Add an error message if authentication fails
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# Mood tracking view
@login_required
def track_mood(request):
    """
    Allows users to track their mood and add a mood note.
    Saves the mood entry and redirects to the mood statistics view.
    """
    if request.method == 'POST':
        mood = request.POST.get('mood')
        mood_note = request.POST.get('mood_note', '')

        # Save the mood entry
        MoodEntry.objects.create(user=request.user, mood=mood, mood_note=mood_note)

        # Redirect to mood statistics after submission
        return redirect('mood_statistics')

    return render(request, 'track_mood.html')


# Mood statistics view with trend analysis
@login_required
def mood_statistics(request):
    """
    Displays mood statistics, trends, and suggestions for the logged-in user.
    """
    # Get all mood entries for the current user
    mood_data = MoodEntry.objects.filter(user=request.user)

    # Count the occurrence of each mood (using F expression for clarity)
    from django.db.models import F
    mood_count = (
        mood_data.values('mood')
        .annotate(count=F('id')).order_by('-count')  # Optimized count using F('id')
    )

    # Get the latest mood entry
    latest_mood = mood_data.last()

    # Get mood trend over the past week (or another time period)
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_moods = mood_data.filter(timestamp__gte=one_week_ago).order_by('timestamp')

    # Calculate mood trends using same optimized count approach
    mood_trend = (
        recent_moods.values('mood')
        .annotate(count=F('id')).order_by('timestamp')
    )

    # Analyze trends (e.g., frequent stress, happiness, or sadness)
    trend_analysis = {
        'high_stress': recent_moods.filter(mood='stressed').count() > 2,
        'recurrent_sadness': recent_moods.filter(mood='sad').count() > 2,
        'positive_trend': recent_moods.filter(mood='happy').count() > recent_moods.filter(mood='sad').count(),
    }

    # Get suggestions based on the latest mood; add a check for None
    latest_mood_value = latest_mood.mood if latest_mood else None  # Prevents recursion by checking for None
    mood_suggestions = get_suggestions_based_on_mood(latest_mood_value)

    # Passing data to the template
    return render(request, 'mood_statistics.html', {
        'mood_data': mood_count,
        'latest_mood': latest_mood,
        'trend_analysis': trend_analysis,
        'mood_trend': mood_trend,
        'mood_suggestions': mood_suggestions,
        'recent_moods': recent_moods,
    })


# Function to provide suggestions based on mood
def get_suggestions_based_on_mood(mood):
    """
    Provides suggestions for the user based on their most recent mood.
    """
    suggestions = {
        'happy': [
            "Keep up the positive vibes! 😊",
            "Try a gratitude journal to stay in the moment.",
            "Continue with light exercises like yoga or walking."
        ],
        'excited': [
            "Channel your excitement into a creative project!",
            "Go for a run or do a HIIT workout to harness your energy."
        ],
        'relaxed': [
            "Maintain your calm by meditating for 10 minutes.",
            "Try some deep breathing exercises to stay centered."
        ],
        'neutral': [
            "You're feeling balanced—maybe try reading or journaling.",
            "A light walk could help boost your mood."
        ],
        'stressed': [
            "Take a break! Try breathing exercises or short mindfulness meditation.",
            "Go for a walk to clear your head and reset."
        ],
        'anxious': [
            "Focus on grounding techniques, like breathing or mindfulness.",
            "Progressive muscle relaxation may help reduce anxiety."
        ],
        'sad': [
            "Reach out to someone close to you for support.",
            "Try journaling your thoughts or going for a nature walk."
        ],
        'angry': [
            "Take deep breaths and try a relaxation technique.",
            "Engage in physical exercise like running or boxing to let off steam."
        ],
        'frustrated': [
            "Step away from the situation causing frustration and take a mental break.",
            "Consider trying yoga or mindfulness meditation to regain focus."
        ],
        'tired': [
            "Make sure you're getting enough sleep and rest.",
            "Engage in low-intensity activities like stretching or yoga."
        ]
    }

    return suggestions.get(mood, ["Take care of yourself, and remember to stay balanced."])
