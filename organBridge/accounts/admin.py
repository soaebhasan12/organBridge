from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'blood_type', 'city', 'is_active']
    list_filter = ['user_type', 'blood_type', 'is_active']
    search_fields = ['username', 'email', 'city']
    fieldsets = UserAdmin.fieldsets + (
        ('OrganBridge Info', {
            'fields': ('user_type', 'phone_number', 'date_of_birth', 'age', 'gender', 'blood_type', 'race', 'city', 'state', 'location')
        }),
    )