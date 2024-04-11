from django.urls import path
from .views import book_list, upload_book, download_book, delete_book, view_book, share_book, rate_book

app_name= 'books'
urlpatterns = [
    path('', book_list, name='file_list'),
    path('upload/', upload_book, name='upload_file'),
    path('download/<str:unique_token>/', download_book, name='download_file'),
    path('delete/<str:unique_token>/', delete_book, name='delete_file'),
    path('view_file/<str:unique_token>/', view_book, name='view_file'),
    path('share_file/<str:unique_token>/', share_book, name='share_file'),
    path('rate_book/<str:unique_token>/', rate_book, name='rate_book'),
]