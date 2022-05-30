import django_eventstream as dje
from django.conf import settings
from loguru import logger
from django_eventstream.channelmanager import DefaultChannelManager
from rest_framework.authtoken.models import Token

from feedapp import models, views


class ChannelAuthManager(DefaultChannelManager):
    def can_read_channel(self, user, channel):
        try:
            role, token_str = channel.split("-")
            if not role or not token_str:
                raise ValueError("Invalid channel format")
        except Exception as e:
            return False

        # check if role is ok
        if role not in ["consumer", "producer"] or not token_str:
            return False

        # check if user is valid
        user = Token.objects.get(key=token_str).user
        if not user:
            return False

        return True

    def get_channels_for_request(self, request, view_kwargs):
        # by default, use view keywords, else query params
        if "format-channels" in view_kwargs:
            channels = set()
            for format_channel in view_kwargs["format-channels"]:
                channels.add(format_channel.format(**view_kwargs))
        elif "channels" in view_kwargs:
            channels = set(view_kwargs["channels"])
        elif "channel" in view_kwargs:
            channels = set([view_kwargs["channel"]])
        else:
            channels = set(request.GET.getlist("channel"))

        # in case handling consumer request, add artificial welcome events
        if view_kwargs.get("format-channels")[0].startswith("consumer"):
            _ = self.handle_query_request(request, view_kwargs)
            self.add_artificial_welcome_event("consumer", channels)
        else:
            self.add_artificial_welcome_event("producer", channels)

        return channels

    def add_artificial_welcome_event(self, welcome_type, channels):
        """Make sure the newly created channel is available in storage.

        When creating a new producer/consumer channel, need to wait for an event
        before it naturally gets logged into the storage backend. However, we need
        to have it be available to be discovered by other channels, and receive
        a message. Thus, put an artificial event in the storage backend to simulate
        event propagation.
        """

        storage_backend = dje.utils.get_storage()
        if len(channels) > 1:
            raise RuntimeError(
                "Why are there more than 1 channels? {}".format(channels)
            )
        else:
            channel = list(channels)[0]

        # already in the channel manager, and assume that storage activated
        event_data = {f"hello {welcome_type}": f"{channel}"}
        _ = storage_backend.append_event(channel, "welcome", event_data)

    def handle_query_request(self, request, view_kwargs) -> bool:
        user = Token.objects.get(key=view_kwargs.get("member_id")).user
        if not user or not self.check_consumer_inputs(request):
            return False

        # find an active producer channel for this consumer query (shared cluster)
        producer_channel, cluster, producer = views.find_active_channel(user)
        if not producer_channel:
            # return False
            # should we simply raise an error when nothing is found?
            raise RuntimeError("No producer channel found")

        # acknowledge query since found an active producer
        record = models.QueryRecord(
            task=request.GET.get("task"),
            model=request.GET.get("model"),
            status="pending",
            consumer=user,
            producer=producer,
            cluster=cluster,
        )
        record.save()

        # build data dict to be fed to the event request
        event_data = {
            "qid": record.id,
        }
        # manually unwrap the data from the request
        event_data.update(
            {"data": request.GET.get("data"), "task": request.GET.get("task")}
        )

        # send event to producer channel for query
        dje.send_event(
            producer_channel,
            "message",
            event_data,
        )

        return True

    def check_consumer_inputs(self, request):
        # make sure have both data and task
        return (
            request.GET.get("task") in settings.SUPPORTED_TASKS
            or request.GET.get("model")
        ) and request.GET.get("data")
