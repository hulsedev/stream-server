import functools
from datetime import datetime

import django_eventstream as dje
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cluster, QueryRecord, User


def index(request):
    """NOTHING TO DO HERE."""
    return redirect(settings.HULSE_LANDING_URL)


def find_active_channel(user):
    """Lookup event streams for active producer channels, and find a cluster with
    a producer to which requesting user has access.

    :param user: User posting a query.
    :type user: django.contrib.auth.models.User
    :return: Producer channel name.
    :rtype: str
    """
    # find all events that match the current request
    # find all people
    user_candidate_channels = {}
    for cluster in user.clusters.all():
        for member in cluster.members.all():
            token, created = Token.objects.get_or_create(user=member)
            user_candidate_channels[f"producer-{token.key}"] = (cluster, member)

    if len(user_candidate_channels) == 0:
        return None, None, None

    # print("candidate channels", user_candidate_channels)

    # retrieve all active channels
    condition = functools.reduce(
        lambda q, f: q | Q(channel__startswith=f),
        list(user_candidate_channels),
        Q(),
    )

    # TODO: figure out how to activate storage
    all_channels = dje.models.Event.objects.all()

    active_channels = set(
        [event.channel for event in dje.models.Event.objects.filter(condition).all()]
    )
    # print("active channels", active_channels)
    if len(active_channels) == 0:
        return None, None, None

    # TODO: implement load balancing
    return (
        list(active_channels)[0],
        user_candidate_channels[list(active_channels)[0]][0],
        user_candidate_channels[list(active_channels)[0]][1],
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def handle_result(request):
    """Result posted from host in response to query"""
    if "qid" not in request.data or "result" not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # find the record corresponding to the request
    record = QueryRecord.objects.filter(pk=request.data.get("qid")).first()
    if record.status == "done":
        return Response(
            {"detail": "query already completed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    query_consumer_channel = find_query_consumer_channel(record)
    if not query_consumer_channel:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # send response to the client
    dje.send_event(
        query_consumer_channel,
        "message",
        {
            "qid": record.id,
            "result": request.data.get("result"),
            "cluster": record.cluster.name,
            "producer": record.producer.username,
        },
    )

    # update query record status in db
    record.status = "done"
    record.save()

    return Response(status=status.HTTP_200_OK)


def find_query_consumer_channel(record) -> str:
    """Find active consumer channel to forward query result back to.

    :param record: Status of the query being returned.
    :type record: models.QueryRecord
    :return: Channel name.
    :rtype: str
    """

    # want to check that the channel is open for the user
    token, created = Token.objects.get_or_create(user=record.consumer)
    candidate_channel = f"consumer-{token.key}"

    # expecting a single channel to be found
    active_consumer_channel = dje.models.Event.objects.filter(
        channel__startswith=candidate_channel
    ).first()

    if not active_consumer_channel:
        return None

    return active_consumer_channel.channel


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ping(request):
    return Response({"ping": "pong"}, status=status.HTTP_200_OK)
