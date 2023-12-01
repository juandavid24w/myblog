from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('register/', views.register, name='register'),
    path('blogs', views.get_user_blogs, name='user_blogs'),
    path('blogs/create', views.create_blog, name='create_blog'),
    path('blogs/<id>/', views.blog_detail, name='blog_detail'),
    path('blogs/<id>/update', views.update_blog, name='update_blog'),
    path('blogs/<id>/delete', views.delete_blog, name='delete_blog'),
    path('category/<category>/', views.blog_category, name='blog_category'),
]