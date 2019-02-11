from rest_framework import serializers
from . import exceptions
from cinema.models import Hall
from cinema.models import Movie
from cinema.models import Session
from cinema.models import Ticket
from cinema.models import TicketStatus
from django.contrib.auth.models import User


def get_changed_entity(serializer):
    pk = serializer.context['request'].parser_context['kwargs']['pk']
    if pk:
        return Movie.objects.filter(id=pk).first()
    else:
        return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        extra_kwargs = {
            'email': {'required': True},
        }


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('id', 'name', 'row_count', 'seat_count')


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name', 'duration')

    def validate(self, data):
        entity = get_changed_entity(self)
        if entity and entity.sessions.exists():
            raise exceptions.DeleteOrChangeError
        return data


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'hall', 'movie', 'started_at', 'price', 'tickets')

    def validate(self, data):
        entity = get_changed_entity(self)
        if entity and entity.tickets.exists():
            raise exceptions.DeleteOrChangeError
        return data


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('id', 'name')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'session', 'ticket_status', 'seat_count')


