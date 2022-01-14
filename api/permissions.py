from rest_framework import permissions
from django.contrib.auth.models import User


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if User.objects.filter(username=request.user, is_superuser=True):
            return True


class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if User.objects.filter(username=request.user, is_superuser=True):
            return True


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user == request.user:
            return True
