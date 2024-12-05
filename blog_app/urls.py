from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_author/', views.create_author, name='create_author'),
    path('create_category/', views.create_category, name='create_category'),
    path('create_post/', views.create_post, name='create_post'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]