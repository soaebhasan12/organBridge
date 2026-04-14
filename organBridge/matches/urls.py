from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('find/', views.find_matches, name='find_matches'),
    path('my-matches/', views.my_matches, name='my_matches'),
]