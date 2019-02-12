from rest_framework import permissions
from .models import Ticket


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool((request.user and request.user.is_staff) or request.method in permissions.SAFE_METHODS)


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class BookForSelfOrIsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.data['user'] == request.user.id


class PayForSelfOrIsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = request.parser_context['kwargs']['pk']
        ticket = Ticket.objects.filter(id=pk).first()
        return request.user.is_staff or request.user.id == ticket.user.id
