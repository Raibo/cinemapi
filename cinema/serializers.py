from rest_framework import serializers
from cinema.models import Hall
from cinema.models import Movie
from cinema.models import Session
from cinema.models import Ticket
from cinema.models import TicketStatus
from django.contrib.auth.models import User


def no_validate():
    pass


class CurrentUserSerializer(serializers.ModelSerializer):
    id_1 = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = User
        fields = ('id', 'id_1', 'username', 'email')
        extra_kwargs = {
            'username': {'validators': []},
        }


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('id', 'name', 'row_count', 'seat_count')


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name', 'duration')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'hall', 'movie', 'started_at', 'price')


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('id', 'name')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'session', 'ticket_status', 'seat_count')


