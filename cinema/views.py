from rest_framework import viewsets, mixins, generics, permissions
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Hall
from .models import Movie
from .models import Session
from .models import TicketStatus
from .models import Ticket
from .serializers import CurrentUserSerializer
from .serializers import HallSerializer
from .serializers import MovieSerializer
from .serializers import SessionSerializer
from .serializers import TicketStatusSerializer
from .serializers import TicketSerializer


class CurrentUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        serializer = self.get_serializer(data=vars(user))
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class HallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = (permissions.AllowAny,)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class TicketStatusViewSet(viewsets.ModelViewSet):
    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


