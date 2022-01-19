from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from film_library.api.models import TV, Movie, FilmsWatched, FilmsToWatch


class UserSerializerList(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения списка пользователей или конкретного пользователя
    """

    id = serializers.HyperlinkedIdentityField(view_name='user-detail')
    tv_added = serializers.HyperlinkedRelatedField(many=True, view_name='tv-detail', read_only=True)
    movies_added = serializers.HyperlinkedRelatedField(many=True, view_name='movie-detail', read_only=True)
    films_watched = serializers.HyperlinkedRelatedField(many=True, view_name='user-watched-list', read_only=True)
    films_to_watch = serializers.HyperlinkedRelatedField(many=True, view_name='user-to-watch-list', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'tv_added', 'movies_added',
                  'films_watched', 'films_to_watch']


class UserSerializerCreateDetail(serializers.ModelSerializer):
    """
    Сериализатор, используемый для добавления и редактирования пользователей
    """

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
    """
    Сериализатор, используемый для отображения списка сериалов
    """

    added_by = serializers.ReadOnlyField(source='added_by.username')
    id = serializers.HyperlinkedIdentityField(view_name='tv-detail')

    class Meta:
        model = TV
        fields = ['id', 'title', 'year', 'rating', 'genre', 'number_of_episodes', 'avg_episode_duration', 'added_by']


class TVSerializerDetail(serializers.ModelSerializer):
    """
    Сериализатор, используемый для отображения конкретного сериала
    """

    added_by = serializers.ReadOnlyField(source='added_by.username')

    class Meta:
        model = TV
        fields = ['id', 'title', 'year', 'rating', 'genre', 'number_of_episodes', 'avg_episode_duration', 'added_by']


class MovieSerializerList(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения списка фильмов
    """

    added_by = serializers.ReadOnlyField(source='added_by.username')
    id = serializers.HyperlinkedIdentityField(view_name='movie-detail')

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'rating', 'genre', 'duration', 'added_by']


class MovieSerializerDetail(serializers.ModelSerializer):
    """
    Сериализатор, используемый для отображения конкретного фильма
    """

    added_by = serializers.ReadOnlyField(source='added_by.username')

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'rating', 'genre', 'duration', 'added_by']


class WatchedSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения списка просмотренных фильмов и сериалов
    """

    user = serializers.ReadOnlyField(source='user.username')
    id = serializers.HyperlinkedIdentityField(view_name='watched-detail')

    class Meta:
        model = FilmsWatched
        fields = ['id', 'user', 'tv', 'movie', 'score', 'review']


class TVWatchedSerializerList(WatchedSerializer):
    """
    Сериализатор, используемый для отображения списка просмотренных сериалов
    """

    class Meta:
        model = FilmsWatched
        fields = ['id', 'user', 'tv', 'score', 'review']


class TVWatchedSerializerDetail(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения конкретного просмотренного сериала
    """

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FilmsWatched
        fields = ['id', 'user', 'tv', 'score', 'review']


class MovieWatchedSerializerList(WatchedSerializer):
    """
    Сериализатор, используемый для отображения списка просмотренных фильмов
    """

    class Meta:
        model = FilmsWatched
        fields = ['id', 'user', 'movie', 'score', 'review']


class MovieWatchedSerializerDetail(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения конкретного просмотренного фильма
    """

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FilmsWatched
        fields = ['id', 'user', 'movie', 'score', 'review']


class ToWatchSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения списка фильмов и сериалов желаемых к просмотру
    """

    user = serializers.ReadOnlyField(source='user.username')
    id = serializers.HyperlinkedIdentityField(view_name='to-watch-detail')

    class Meta:
        model = FilmsToWatch
        fields = ['id', 'user', 'tv', 'movie']


class TVToWatchSerializerList(ToWatchSerializer):
    """
    Сериализатор, используемый для отображения списка сериалов желаемых к просмотру
    """

    class Meta:
        model = FilmsToWatch
        fields = ['id', 'user', 'tv']


class TVToWatchSerializerDetail(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения конкретного сериала желаемого к просмотру
    """

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FilmsToWatch
        fields = ['id', 'user', 'tv']


class MovieToWatchSerializerList(ToWatchSerializer):
    """
    Сериализатор, используемый для отображения списка фильмов желаемых к просмотру
    """

    class Meta:
        model = FilmsToWatch
        fields = ['id', 'user', 'movie']


class MovieToWatchSerializerDetail(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор, используемый для отображения конкретного фильма желаемого к просмотру
    """

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FilmsToWatch
        fields = ['id', 'user', 'movie']
