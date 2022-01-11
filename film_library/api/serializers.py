from rest_framework import serializers
from film_library.api.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    tv_added = serializers.PrimaryKeyRelatedField(many=True, queryset=TV.objects.all())
    movies_added = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())
    films_watched = serializers.PrimaryKeyRelatedField(many=True, queryset=FilmsWatched.objects.all())
    films_to_watch = serializers.PrimaryKeyRelatedField(many=True, queryset=FilmsToWatch.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'tv_added', 'movies_added',
                  'films_watched', 'films_to_watch']


class TVSerializer(serializers.ModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.username')

    class Meta:
        model = TV
        fields = ['id', 'title', 'year', 'rating', 'genre', 'number_of_episodes', 'avg_episode_duration', 'added_by']


class MovieSerializer(serializers.ModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.username')

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'rating', 'genre', 'duration', 'added_by']


class WatchedSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FilmsWatched
        fields = ['user', 'tv', 'movie', 'score', 'review']


class TVWatchedSerializer(WatchedSerializer):
    class Meta:
        model = FilmsWatched
        fields = ['user', 'tv', 'score', 'review']


class MovieWatchedSerializer(WatchedSerializer):
    class Meta:
        model = FilmsWatched
        fields = ['user', 'movie', 'score', 'review']


class ToWatchSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FilmsToWatch
        fields = ['user', 'tv', 'movie']


class TVToWatchSerializer(ToWatchSerializer):
    class Meta:
        model = FilmsToWatch
        fields = ['user', 'tv']


class MovieToWatchSerializer(ToWatchSerializer):
    class Meta:
        model = FilmsToWatch
        fields = ['user', 'movie']
