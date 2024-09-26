"""
This module defines the database models for the mental health app.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class MoodEntry(models.Model):
    """
    Model to track mood entries for users.
    """

    # Constants for mood choices
    MOOD_HAPPY = 'happy'
    MOOD_EXCITED = 'excited'
    MOOD_RELAXED = 'relaxed'
    MOOD_NEUTRAL = 'neutral'
    MOOD_STRESSED = 'stressed'
    MOOD_ANXIOUS = 'anxious'
    MOOD_SAD = 'sad'
    MOOD_ANGRY = 'angry'
    MOOD_FRUSTRATED = 'frustrated'
    MOOD_TIRED = 'tired'

    MOOD_CHOICES = [
        (MOOD_HAPPY, 'Happy'),
        (MOOD_EXCITED, 'Excited'),
        (MOOD_RELAXED, 'Relaxed'),
        (MOOD_NEUTRAL, 'Neutral'),
        (MOOD_STRESSED, 'Stressed'),
        (MOOD_ANXIOUS, 'Anxious'),
        (MOOD_SAD, 'Sad'),
        (MOOD_ANGRY, 'Angry'),
        (MOOD_FRUSTRATED, 'Frustrated'),
        (MOOD_TIRED, 'Tired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES)
    mood_note = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.mood} - {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']  # Order by latest entries first

class UserProfile(models.Model):
    """
    User profile model to store additional information.

    Attributes:
        user: The user associated with this profile.
        age: The age of the user.
        gender: The gender of the user.
        created_at: Timestamp when the profile was created.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(null=True, blank=True)

    # Consider using choices for gender
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non-binary', 'Non-binary'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def clean(self):
        """Custom validation to ensure age is a positive integer."""
        if self.age is not None and self.age < 0:
            raise ValidationError('Age cannot be negative.')

class Session(models.Model):
    """
    Model to track user sessions.

    Attributes:
        user: The user associated with this session.
        date: Timestamp when the session was created.
        notes: Additional notes about the session.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Session for {self.user.username} on {self.date}'
    