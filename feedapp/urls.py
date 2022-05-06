from django.urls import path

from feedapp import events, views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "consumer/<member_id>/",
        events.handle_consumer_event,
        {"format-channels": ["consumer-{member_id}"]},
    ),
    path(
        "producer/<member_id>/",
        events.handle_producer_event,
        {"format-channels": ["producer-{member_id}"]},
    ),
    path("ping/", views.ping, name="ping"),
]
