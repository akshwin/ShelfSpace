from django.urls import path
from . import views

app_name = 'ShelfSpaceBlogs'
urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('', views.post_list, name='post_list'),
    path('upvote/<int:post_id>/', views.upvote_post, name='upvote_post'),
]
