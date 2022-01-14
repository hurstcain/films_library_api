from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from film_library.api.models import TV, Movie, FilmsWatched, FilmsToWatch
import film_library.api.serializers as ser
from film_library.api.permissions import IsSuperuser, IsSuperuserOrReadOnly, IsCreatorOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'login': reverse('admin:index', request=request, format=format),
        'tv list': reverse('tv-list', request=request, format=format),
        'movie list': reverse('movie-list', request=request, format=format),
        'your tv and movie watched list': reverse('watched-list', request=request, format=format),
        'your tv watched list': reverse('tv-watched-list', request=request, format=format),
        'your movie watched list': reverse('movie-watched-list', request=request, format=format),
        'your tv and movie to watch list': reverse('to-watch-list', request=request, format=format),
        'your tv to watch list': reverse('tv-to-watch-list', request=request, format=format),
        'your movie to watch list': reverse('movie-to-watch-list', request=request, format=format),
        'users list (only for admin)': reverse('user-list', request=request, format=format),
    })


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsSuperuser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ser.UserSerializerList
        elif self.request.method == 'POST':
            return ser.UserSerializerCreateDetail


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ser.UserSerializerCreateDetail
    permission_classes = [IsSuperuser]


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = ser.MovieSerializerList
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = ser.MovieSerializerDetail
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class TVList(generics.ListCreateAPIView):
    queryset = TV.objects.all()
    serializer_class = ser.TVSerializerList
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class TVDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TV.objects.all()
    serializer_class = ser.TVSerializerDetail
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class WatchedList(generics.ListAPIView):
    serializer_class = ser.WatchedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(user=self.request.user)


class WatchedDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def get_queryset(self):
        return FilmsWatched.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        obj = FilmsWatched.objects.filter(pk=int(self.kwargs['pk']))

        if obj[0].is_tv():
            return ser.TVWatchedSerializerDetail
        elif obj[0].is_movie():
            return ser.MovieWatchedSerializerDetail


class AllUsersWatchedDetail(WatchedDetail):
    def get_queryset(self):
        return FilmsWatched.objects.all()


class TVWatchedList(generics.ListCreateAPIView):
    serializer_class = ser.TVWatchedSerializerList
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(tv__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieWatchedList(generics.ListCreateAPIView):
    serializer_class = ser.MovieWatchedSerializerList
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(movie__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToWatchList(generics.ListAPIView):
    serializer_class = ser.ToWatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(user=self.request.user)


class ToWatchDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        obj = FilmsToWatch.objects.filter(pk=int(self.kwargs['pk']))

        if obj[0].is_tv():
            return ser.TVToWatchSerializerDetail
        elif obj[0].is_movie():
            return ser.MovieToWatchSerializerDetail


class AllUsersToWatchDetail(ToWatchDetail):
    def get_queryset(self):
        return FilmsToWatch.objects.all()


class TVToWatchList(generics.ListCreateAPIView):
    serializer_class = ser.TVToWatchSerializerList
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(tv__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieToWatchList(generics.ListCreateAPIView):
    serializer_class = ser.MovieToWatchSerializerList
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(movie__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
