from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from film_library.api.models import *


class UserSerializerList(serializers.HyperlinkedModelSerializer):
    tv_added = serializers.HyperlinkedRelatedField(many=True, view_name='tv-detail', read_only=True)
    movies_added = serializers.HyperlinkedRelatedField(many=True, view_name='movie-detail', read_only=True)
    films_watched = serializers.HyperlinkedRelatedField(many=True, view_name='user-watched-list', read_only=True)
    films_to_watch = serializers.HyperlinkedRelatedField(many=True, view_name='to-watch-detail', read_only=True)
    id = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'tv_added', 'movies_added',
                  'films_watched', 'films_to_watch']


class UserSerializerCreateDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_superuser',
                  'is_staff', 'is_active']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
                'style': {'input_type': 'password', 'placeholder': 'Password'}
            }
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializerCreateDetail, self).create(validated_data)


class TVSerializerList(serializers.HyperlinkedModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.username')
    id = serializers.HyperlinkedIdentityField(view_name='tv-detail')

    class Meta:
        model = TV
        fields = ['id', 'title', 'year', 'rating', 'genre', 'number_of_episodes', 'avg_episode_duration', 'added_by']


class TVSerializerDetail(serializers.ModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.username')

    class Meta:
        model = TV
        fields = ['id', 'title', 'year', 'rating', 'genre', 'number_of_episodes', 'avg_episode_duration', 'added_by']


class MovieSerializerList(serializers.HyperlinkedModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.username')
    id = serializers.HyperlinkedIdentityField(view_name='movie-detail')

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'rating', 'genre', 'duration', 'added_by']


class MovieSerializerDetail(serializers.ModelSerializer):
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
