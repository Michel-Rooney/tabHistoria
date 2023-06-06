from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('', include('apps.post.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('client/', include('apps.client.urls')),
]
