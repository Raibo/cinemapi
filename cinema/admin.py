from django.contrib import admin
from cinema.models import Hall
from cinema.models import Movie
from cinema.models import Session
from cinema.models import TicketStatus
from cinema.models import Ticket


admin.site.register(Hall)
admin.site.register(Movie)
admin.site.register(Session)
admin.site.register(TicketStatus)
admin.site.register(Ticket)

