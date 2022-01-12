from rest_framework import generics
from rest_framework import permissions
from film_library.api.serializers import *
from film_library.api.permissions import IsSuperuser, IsSuperuserOrReadOnly


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperuser]


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class TVList(generics.ListCreateAPIView):
    queryset = TV.objects.all()
    serializer_class = TVSerializer
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class WatchedList(generics.ListAPIView):
    serializer_class = WatchedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(user=self.request.user)


class TVWatchedList(generics.ListCreateAPIView):
    serializer_class = TVWatchedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(tv__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieWatchedList(generics.ListCreateAPIView):
    serializer_class = MovieWatchedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(movie__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToWatchList(generics.ListAPIView):
    serializer_class = ToWatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(user=self.request.user)


class TVToWatchList(generics.ListCreateAPIView):
    serializer_class = TVToWatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(tv__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieToWatchList(generics.ListCreateAPIView):
    serializer_class = MovieToWatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(movie__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
