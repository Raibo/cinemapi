from django.db.models import ProtectedError
from rest_framework import viewsets, mixins, generics, permissions, status
from rest_framework.views import exception_handler
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from . import custom_permissions
from . import exceptions
from django.contrib.auth.models import User
from .models import Hall
from .models import Movie
from .models import Session
from .models import TicketStatus
from .models import Ticket
from .serializers import UserSerializer
from .serializers import HallSerializer
from .serializers import MovieSerializer
from .serializers import SessionSerializer
from .serializers import TicketStatusSerializer
from .serializers import TicketSerializer


def check_delete_integrity(func):
    def decorator(class_instance, obj_instance):
        try:
            func(class_instance, obj_instance)
        except ProtectedError:
            raise exceptions.DeleteOrChangeError
    return decorator


class CurrentUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class HallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = (permissions.AllowAny,)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (custom_permissions.StaffOrReadOnly,)

    @check_delete_integrity
    def perform_destroy(self, instance):
        super(MovieViewSet, self).perform_destroy(instance)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (custom_permissions.StaffOrReadOnly,)

    @check_delete_integrity
    def perform_destroy(self, instance):
        super(SessionViewSet, self).perform_destroy(instance)


class TicketStatusViewSet(viewsets.ModelViewSet):
    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


