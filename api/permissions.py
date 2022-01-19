from rest_framework import permissions
from django.contrib.auth.models import User


class IsSuperuser(permissions.BasePermission):
    """
    Разрешение только для суперпользователей
    """

    def has_permission(self, request, view):
        if User.objects.filter(username=request.user, is_superuser=True):
            return True


class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Разрешение для суперпользователей на чтение/запись.
    Разрешение только для чтения, если не суперпользователь.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if User.objects.filter(username=request.user, is_superuser=True):
            return True


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Разрешение для создателей на чтение/запись.
    Разрешение только для чтения, если не создатель.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user == request.user:
            return True
