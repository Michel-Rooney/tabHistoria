from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('post/', views.post, name='post'),
    path('post/<int:id>/', views.post_viewer, name='post_viewer')
]
