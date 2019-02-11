from django.db import models


class Hall(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    row_count = models.IntegerField(null=False, blank=False)
    seat_count = models.IntegerField(null=False, blank=False)


class Movie(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    duration = models.DurationField(null=False, blank=False)


class Session(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, null=False, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=False, blank=False)
    started_at = models.DateTimeField(null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)


class TicketStatus(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)


class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT, null=False, blank=False)
    ticket_status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT, null=False, blank=False)
