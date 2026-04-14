from django.urls import path
from . import views

app_name = 'ml_model'

urlpatterns = [
    path('status/', views.model_status, name='model_status'),
]