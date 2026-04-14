from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profiles.urls', namespace='profiles')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('matches/', include('matches.urls', namespace='matches')),
    path('ml/', include('ml_model.urls', namespace='ml_model')),
    path('bias/', include('bias_dashboard.urls', namespace='bias_dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)