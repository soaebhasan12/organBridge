from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

CustomUser = get_user_model()


class OrganMatch(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    )

    donor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='donor_matches',
        limit_choices_to={'user_type': 'donor'}
    )
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipient_matches',
        limit_choices_to={'user_type': 'recipient'}
    )
    match_score = models.FloatField(help_text="ML compatibility score (0-100)")
    organs_matched = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    class Meta:
        unique_together = ('donor', 'recipient')
        ordering = ['-match_score', '-created_at']

    def __str__(self):
        return f"{self.donor.username} → {self.recipient.username} ({self.match_score}%)"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at


class MatchMessage(models.Model):
    match = models.ForeignKey(OrganMatch, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username}"


class MatchPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    max_distance = models.IntegerField(default=100)
    min_match_score = models.IntegerField(default=70)
    notify_new_matches = models.BooleanField(default=True)
    notify_messages = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"