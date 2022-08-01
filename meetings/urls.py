"""meetings URL Configuration
"""
from . import views
from django.urls import path, include
from rest_framework import routers
from meetings import views
from rest_framework_extensions.routers import NestedRouterMixin

router = routers.DefaultRouter()
router.register(r'Minute', views.MinuteView, 'Minute')
router.register(r'MinuteItem', views.MinuteView, 'MinuteItem')
router.register(r'PrivateMeeting', views.PrivateMeetingView, 'PrivateMeeting')
router.register(r'Meeting', views.MeetingView, 'meeting')
router.register(r'Agenda', views.AgendaView, 'Agenda')
router.register(r'AgendaItem', views.AgendaItemView, 'AgendaItem')

class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass

router = NestedDefaultRouter()

meeting_router = router.register(r'Meeting', views.MeetingView, 'meeting')
meeting_router.register(
    r'Agenda',
    views.AgendaView,
    basename='meeting-agenda',
    parents_query_lookups=['meeting']
).register(
    'AgendaItem',
    views.AgendaItemView,
    basename='meeting-agenda-agendaitem',
    parents_query_lookups=['agenda','agenda_id']
)
meeting_router.register(
    'Minute',
    views.MinuteView,
    basename='meeting-minutes',
    parents_query_lookups=['meeting']
).register(
    'MinuteItem',
    views.MinuteItemView,
    basename='meeting-minute-minuteitem',
    parents_query_lookups=['minute','minute_id']
)

private_meeting_router = router.register(r'PrivateMeeting', views.PrivateMeetingView, 'PrivateMeeting')
private_meeting_router.register(
    'Agenda',
    views.AgendaView,
    basename='pmeeting-agenda',
    parents_query_lookups=['meeting']
).register(
    'AgendaItem',
    views.AgendaItemView,
    basename='pmeeting-agenda-agendaitem',
    parents_query_lookups=['agenda','agenda_id']
)
private_meeting_router.register(
    'Minute',
    views.MinuteView,
    basename='pmeeting-minutes',
    parents_query_lookups=['meeting']
).register(
    'MinuteItem',
    views.MinuteItemView,
    basename='meeting-minute-minuteitem',
    parents_query_lookups=['minute','minute_id']
)


urlpatterns = [
    path('', include(router.urls)),
]
