from django.urls import path
from . import views


urlpatterns = [
    path('profile/<int:id>/', views.profile, name='profile'),
    path('post/', views.post, name='post'),
    path('post/<int:id>/', views.post_viewer, name='post_viewer'),
    path('vote/<int:id>/', views.vote, name='vote'),
    path('comment/<int:id>/', views.comment, name='comment'),
    path('render_post/<int:id>/', views.render_post, name='render_post'),
]
