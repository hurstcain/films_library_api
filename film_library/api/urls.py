from django.urls import path
from django.contrib import admin
from film_library.api.views import *

urlpatterns = [
    path('login/', admin.site.urls),
    path('user/', UserList.as_view()),
    path('movie/', MovieList.as_view()),
    path('tv/', TVList.as_view()),
    path('watched_list/', WatchedList.as_view()),
    path('watched_list/movie/', MovieWatchedList.as_view()),
    path('watched_list/tv/', TVWatchedList.as_view()),
    path('to_watch_list/', ToWatchList.as_view()),
    path('to_watch_list/movie', MovieToWatchList.as_view()),
    path('to_watch_list/tv', TVToWatchList.as_view()),
]
