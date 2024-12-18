from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_user/', views.create_user, name='create_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_category/', views.create_category, name='create_category'),
    path('create_post/', views.create_post, name='create_post'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('about/', views.about, name='about'),
    path('users/', views.user_list, name='user_list'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/confirm_delete/', views.confirm_delete_post, name='confirm_delete_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]