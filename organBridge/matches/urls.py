from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('find/', views.find_matches, name='find_matches'),
    path('my-matches/', views.my_matches, name='my_matches'),
    path('match/<int:match_id>/<str:status>/', views.update_match_status, name='update_match_status'),
    path('explanation/<int:match_id>/', views.get_ai_explanation, name='get_ai_explanation'),
]