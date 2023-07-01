from django.urls import path
from . import views


app_name = 'client'

urlpatterns = [
    path('profile/<int:id>/', views.profile, name='profile'),
    path('update_profile/<int:id>/',
         views.update_profile, name='update_profile'),
]
