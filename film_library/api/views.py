from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from film_library.api.models import TV, Movie, FilmsWatched, FilmsToWatch
import film_library.api.serializers as ser
from film_library.api.permissions import IsSuperuser, IsSuperuserOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'login': reverse('admin:index', request=request, format=format),
        'tv': reverse('tv-list', request=request, format=format),
        'movie': reverse('movie-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ser.UserSerializerList
    permission_classes = [IsSuperuser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ser.UserSerializer
    permission_classes = [IsSuperuser]


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = ser.MovieSerializer
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = ser.MovieSerializer
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class TVList(generics.ListCreateAPIView):
    queryset = TV.objects.all()
    serializer_class = ser.TVSerializer
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class TVDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TV.objects.all()
    serializer_class = ser.TVSerializer
    permission_classes = [IsSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class WatchedList(generics.ListAPIView):
    serializer_class = ser.WatchedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(user=self.request.user)


class WatchedDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        obj = FilmsWatched.objects.filter(pk=int(self.kwargs['pk']))

        if obj[0].is_tv():
            return ser.TVWatchedSerializer
        elif obj[0].is_movie():
            return ser.MovieWatchedSerializer


class TVWatchedList(generics.ListCreateAPIView):
    serializer_class = ser.TVWatchedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsWatched.objects.filter(tv__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieWatchedList(generics.ListCreateAPIView):
    serializer_class = ser.MovieWatchedSerializer
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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # print(self.request.get_full_path())
        # if self.request.get_full_path() == '/user/':
        #     return FilmsToWatch.objects.all()
        # else:
        return FilmsToWatch.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        obj = FilmsToWatch.objects.filter(pk=int(self.kwargs['pk']))

        if obj[0].is_tv():
            return ser.TVToWatchSerializer
        elif obj[0].is_movie():
            return ser.MovieToWatchSerializer


class TVToWatchList(generics.ListCreateAPIView):
    serializer_class = ser.TVToWatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(tv__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieToWatchList(generics.ListCreateAPIView):
    serializer_class = ser.MovieToWatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmsToWatch.objects.filter(movie__isnull=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
