from rest_framework import serializers
from film_library.api.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active']


class UserSerializerList(serializers.HyperlinkedModelSerializer):
    tv_added = serializers.HyperlinkedRelatedField(many=True, view_name='tv-detail', read_only=True)
    movies_added = serializers.HyperlinkedRelatedField(many=True, view_name='movie-detail', read_only=True)
    films_watched = serializers.HyperlinkedRelatedField(many=True, view_name='watched-detail', read_only=True)
    films_to_watch = serializers.HyperlinkedRelatedField(many=True, view_name='to-watch-detail', read_only=True)

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


class WatchedSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    id = serializers.HyperlinkedIdentityField(view_name='watched-detail')

    class Meta:
        model = FilmsWatched
        fields = ['id', 'user', 'tv', 'movie', 'score', 'review']


class TVWatchedSerializer(WatchedSerializer):
    class Meta:
        model = FilmsWatched
        fields = ['id', 'user', 'tv', 'score', 'review']


class MovieWatchedSerializer(WatchedSerializer):
    class Meta:
        model = FilmsWatched
        fields = ['id', 'user', 'movie', 'score', 'review']


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
