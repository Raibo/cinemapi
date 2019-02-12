from django.db import models
from django.contrib.auth.models import User


class Hall(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    row_count = models.IntegerField(null=False, blank=False)
    seat_count = models.IntegerField(null=False, blank=False)


class Movie(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    duration = models.DurationField(null=False, blank=False)


class Session(models.Model):
    hall = models.ForeignKey(Hall, related_name='sessions', on_delete=models.PROTECT, null=False, blank=False)
    movie = models.ForeignKey(Movie, related_name='sessions', on_delete=models.PROTECT, null=False, blank=False)
    started_at = models.DateTimeField(null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)


class TicketStatus(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)


class Ticket(models.Model):
    session = models.ForeignKey(Session, related_name='tickets', on_delete=models.PROTECT, null=False, blank=False)
    user = models.ForeignKey(User, related_name='tickets', on_delete=models.PROTECT, null=False, blank=False)
    ticket_status = models.ForeignKey(TicketStatus, related_name='status', on_delete=models.PROTECT, null=False, blank=False)
    row = models.IntegerField(null=False, blank=False)
    seat = models.IntegerField(null=False, blank=False)
