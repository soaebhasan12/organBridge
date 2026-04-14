from django.urls import path
from . import views

app_name = 'bias_dashboard'

urlpatterns = [
    path('', views.bias_overview, name='bias_overview'),
]