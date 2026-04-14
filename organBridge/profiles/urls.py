from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/dashboard/', views.profile_dashboard, name='profile_dashboard'),
    path('profiles/setup/', views.profile_setup, name='profile_setup'),
    path('profiles/edit/', views.edit_profile, name='edit_profile'),
]