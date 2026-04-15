from django.contrib import admin
from .models import OrganMatch, MatchMessage, MatchPreference


@admin.register(OrganMatch)
class OrganMatchAdmin(admin.ModelAdmin):
    list_display = ['donor', 'recipient', 'match_score', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['donor__username', 'recipient__username']


@admin.register(MatchMessage)
class MatchMessageAdmin(admin.ModelAdmin):
    list_display = ['match', 'sender', 'timestamp', 'is_read']
    list_filter = ['is_read']


@admin.register(MatchPreference)
class MatchPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'max_distance', 'min_match_score']