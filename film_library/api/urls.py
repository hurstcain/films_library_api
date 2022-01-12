from django.urls import path
from django.contrib import admin
import film_library.api.views as views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('login/', admin.site.urls, name='admin'),
    path('user/', views.UserList.as_view(), name='user-list'),
    path('user/<pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('movie/', views.MovieList.as_view(), name='movie-list'),
    path('movie/<pk>/', views.MovieDetail.as_view(), name='movie-detail'),
    path('tv/', views.TVList.as_view(), name='tv-list'),
    path('tv/<pk>/', views.TVDetail.as_view(), name='tv-detail'),
    path('watched_list/', views.WatchedList.as_view(), name='watched-list'),
    path('watched_list/movie/', views.MovieWatchedList.as_view(), name='movie-watched-list'),
    path('watched_list/tv/', views.TVWatchedList.as_view(), name='tv-watched-list'),
    path('watched_list/<pk>/', views.WatchedDetail.as_view(), name='watched-detail'),
    path('to_watch_list/', views.ToWatchList.as_view(), name='to-watch-list'),
    path('to_watch_list/movie/', views.MovieToWatchList.as_view(), name='movie-to-watch-list'),
    path('to_watch_list/tv/', views.TVToWatchList.as_view(), name='tv-to-watch-list'),
    path('to_watch_list/<pk>/', views.ToWatchDetail.as_view(), name='to-watch-detail'),
]
