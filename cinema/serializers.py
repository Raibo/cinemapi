import datetime
from django.db.models import F, Q
from cinemapi.settings import CINEMA
from rest_framework import serializers
from . import exceptions
from cinema.models import Hall
from cinema.models import Movie
from cinema.models import Session
from cinema.models import Ticket
from cinema.models import TicketStatus
from django.contrib.auth.models import User


def get_changed_entity(serializer):
    pk = None
    try:
        pk = serializer.context['request'].parser_context['kwargs']['pk']
    finally:
        if pk:
            return Movie.objects.filter(id=pk).first()
        else:
            return None


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True, 'write_only': True},
        }


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('id', 'name', 'row_count', 'seat_count')


class MovieSerializer(serializers.ModelSerializer):
    def validate(self, data):
        entity = get_changed_entity(self)
        if entity and entity.sessions.exists():
            raise exceptions.DeleteOrChangeError
        return data

    class Meta:
        model = Movie
        fields = ('id', 'name', 'duration')


class NestedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('row', 'seat')


class SessionSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField()

    def get_tickets(self, session):
        qs = session.tickets
        return NestedTicketSerializer(qs, many=True, read_only=True).data

    def validate(self, data):
        entity = get_changed_entity(self)
        if entity and entity.tickets.exists():
            raise exceptions.DeleteOrChangeError

        started_at = data['started_at']
        duration = Movie.objects.filter(id=data['movie'].id).first().duration
        additional_time = CINEMA['SESSION_ADDITIONAL_TIME']

        start_time = started_at - started_at.replace(hour=0, minute=0, second=0, microsecond=0)
        finish_time = start_time + duration + additional_time

        if start_time < CINEMA['CINEMA_OPENS_AT'] or finish_time > CINEMA['CINEMA_CLOSES_AT']:
            raise exceptions.SessionTimeError

        if Session.objects.filter(
                ~(Q(started_at__gte=started_at+duration+additional_time)
                  | Q(started_at__lte=started_at-F('movie__duration')-additional_time))
        ).exists():
            raise exceptions.SessionIntersectError

        return data

    class Meta:
        model = Session
        fields = ('id', 'hall', 'movie', 'started_at', 'price', 'tickets')


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('id', 'name')


class NestedTicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('id', 'name')


class TicketSerializer(serializers.ModelSerializer):
    ticket_status = serializers.SerializerMethodField()

    def get_ticket_status(self, ticket):
        qs = ticket.ticket_status
        return NestedTicketStatusSerializer(qs, many=False, read_only=True).data

    @staticmethod
    def check_time(time):
        tz = datetime.timezone(datetime.timedelta(minutes=0))
        started_at = time.astimezone(tz).replace(tzinfo=None)
        now = datetime.datetime.now(tz=tz).replace(tzinfo=None)

        if started_at - CINEMA['BOOK_TIME_THRESHOLD'] < now:
            raise exceptions.BookTooLateError

    def validate(self, data):
        data['ticket_status'] = TicketStatus.objects.filter(id=CINEMA['BOOKED_STATUS_ID']).first()
        hall = data['session'].hall

        self.check_time(data['session'].started_at)

        if data['row'] <= 0 or data['row'] > hall.row_count or data['seat'] <= 0 or data['seat'] > hall.seat_count:
            raise exceptions.WrongSeatError

        if Ticket.objects.filter(Q(session_id=data['session']) & Q(row=data['row']) & Q(seat=data['seat'])):
            raise exceptions.WrongSeatError

        return data

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'session', 'ticket_status', 'row', 'seat')


class TicketPaySerializer(TicketSerializer):
    def validate(self, data):
        super().check_time(self.instance.session.started_at)

        payed_status_id = CINEMA['PAYED_STATUS_ID']
        if self.instance.ticket_status.id == payed_status_id:
            raise exceptions.AlreadyPaidError

        ticket_status = TicketStatus.objects.filter(id=payed_status_id).first()
        return {'ticket_status': ticket_status}
