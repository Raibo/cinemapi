from cinemapi.settings import CINEMA
from django.db.models import ProtectedError
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
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
from .serializers import TicketPaySerializer


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


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (custom_permissions.IsStaff,)


class HallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = (permissions.AllowAny,)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (custom_permissions.IsStaffOrReadOnly,)

    @check_delete_integrity
    def perform_destroy(self, instance):
        super(MovieViewSet, self).perform_destroy(instance)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (custom_permissions.IsStaffOrReadOnly,)

    @check_delete_integrity
    def perform_destroy(self, instance):
        super(SessionViewSet, self).perform_destroy(instance)


class TicketStatusViewSet(viewsets.ModelViewSet):
    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer


class TicketViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects
        else:
            return Ticket.objects.filter(user=self.request.user)


class BookViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TicketSerializer
    permission_classes = (custom_permissions.BookForSelfOrIsStaff,)


class PayViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = TicketPaySerializer
    permission_classes = (custom_permissions.PayForSelfOrIsStaff,)
    queryset = Ticket.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if not partial:
            raise exceptions.PayOnlyPatchError

        instance = self.get_object()
        serializer = self.get_serializer(instance, data={}, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data)
