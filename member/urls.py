from django.urls import path
from . import views


urlpatterns = [
    path('profile/<int:id>/', views.profile, name='profile'),
    path('post/', views.post, name='post'),
    path('post/<int:id>/', views.post_viewer, name='post_viewer'),
    path('vote/<int:id>/', views.vote, name='vote'),
    path('comment/<int:id>/', views.comment, name='comment'),
    path('render_post/<int:id>/', views.render_post, name='render_post'),
    path('delete_post/<int:pk_post>/<int:pk_member>/', views.delete_post, name='delete_post'),
    path('update_post/<int:pk_post>/<int:pk_member>/', views.update_post, name='update_post'),
]
