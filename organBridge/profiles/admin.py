from django.contrib import admin
from .models import DonorProfile, RecipientProfile


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'health_status', 'is_available', 'willing_to_travel', 'created_at']
    list_filter = ['health_status', 'is_available', 'smoking_status', 'alcohol_use']
    search_fields = ['user__username', 'user__city']


@admin.register(RecipientProfile)
class RecipientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'urgency_level', 'current_hospital', 'created_at']
    list_filter = ['urgency_level', 'insurance_coverage']
    search_fields = ['user__username', 'user__city']