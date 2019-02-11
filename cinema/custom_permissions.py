from rest_framework import permissions


class StaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool((request.user and request.user.is_staff) or request.method in permissions.SAFE_METHODS)
