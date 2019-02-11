from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('current_user', views.CurrentUserViewSet, basename='current_user')
router.register('register', views.CreateUserViewSet, basename='register')
router.register('hall', views.HallViewSet)
router.register('movie', views.MovieViewSet)
router.register('session', views.SessionViewSet)
router.register('ticket_status', views.TicketStatusViewSet)
router.register('ticket', views.TicketViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
