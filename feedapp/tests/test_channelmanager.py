import uuid
from unittest import skip

import django_eventstream as dje
from django.test import TestCase, RequestFactory
from rest_framework.authtoken.models import Token

from feedapp.models import User, Cluster
from feedapp.channelmanager import ChannelAuthManager
from feedapp.tests import config


class ChannelManagerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            config.username, config.email, config.password
        )
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.cluster = self.create_cluster()
        self.channel_manager = ChannelAuthManager()
        self.headers = {"HTTP_AUTHORIZATION": f"Token {self.token}"}
        self.factory = RequestFactory(**self.headers)
        self.dje_storage = dje.utils.get_storage()

    def create_cluster(self, user=None):
        user = user if user else self.user
        new_cluster = Cluster(
            name=config.name, description=config.description, admin=user
        )
        new_cluster.save()
        new_cluster.members.add(user)
        new_cluster.save()

        return new_cluster

    def test_read_consumer_channel_success(self):
        channel = "consumer-{}".format(self.token.key)
        self.assertTrue(self.channel_manager.can_read_channel(self.user, channel))

    def test_read_producer_channel_success(self):
        channel = "producer-{}".format(self.token.key)
        self.assertTrue(self.channel_manager.can_read_channel(self.user, channel))

    def test_read_channel_consumer_wrong_key(self):
        channel = "consumer-{}".format(uuid.uuid4())
        self.assertFalse(self.channel_manager.can_read_channel(self.user, channel))

    def test_read_channel_producer_wrong_key(self):
        channel = "consumer-{}".format(uuid.uuid4())
        self.assertFalse(self.channel_manager.can_read_channel(self.user, channel))

    def test_read_channel_wrong_user_type(self):
        channel = "somethingelse-{}".format(self.token.key)
        self.assertFalse(self.channel_manager.can_read_channel(self.user, channel))

    def test_read_channel_wrong_format(self):
        channel = "producer"
        self.assertFalse(self.channel_manager.can_read_channel(self.user, channel))

    def setup_producer_channel(self):
        channel = "producer-{}".format(self.token.key)
        view_kwargs = {"format-channels": [channel], "member_id": self.token.key}
        mock_request = self.factory.get(
            f"/producer/{self.token.key}/", data=config.get_query_data()
        )
        mock_request.user = self.user
        _ = self.channel_manager.get_channels_for_request(mock_request, view_kwargs)

    def test_get_channels_consumer_success(self):
        # setup a producer channel
        self.setup_producer_channel()
        channel = "consumer-{}".format(self.token.key)
        view_kwargs = {"format-channels": [channel], "member_id": self.token.key}
        mock_request = self.factory.get(
            f"/consumer/{self.token.key}/", data=config.get_query_data()
        )
        mock_request.user = self.user
        channels = self.channel_manager.get_channels_for_request(
            mock_request, view_kwargs
        )
        self.assertEqual(len(channels), 1)
        self.assertEqual(list(channels)[0], channel)

        # make sure events are consistently displayed
        stored_events = dje.models.Event.objects.all()
        # 2 producer welcome, 1 query event, 2 consumer welcome
        self.assertEqual(len(stored_events), 5)
        self.assertEqual(stored_events[4].type, "welcome")

    def test_get_channels_consumer_no_producer(self):
        channel = "consumer-{}".format(self.token.key)
        view_kwargs = {"format-channels": [channel], "member_id": self.token.key}
        mock_request = self.factory.get(
            f"/consumer/{self.token.key}/", data=config.get_query_data()
        )
        mock_request.user = self.user
        was_raised = False
        try:
            _ = self.channel_manager.get_channels_for_request(mock_request, view_kwargs)
        except RuntimeError as e:
            was_raised = True
        self.assertTrue(was_raised)

    def test_get_channels_producer_success(self):
        channel = "producer-{}".format(self.token.key)
        view_kwargs = {"format-channels": [channel], "member_id": self.token.key}
        mock_request = self.factory.get(
            f"/producer/{self.token.key}/", data=config.get_query_data()
        )
        mock_request.user = self.user
        channels = self.channel_manager.get_channels_for_request(
            mock_request, view_kwargs
        )
        self.assertEqual(len(channels), 1)
        self.assertEqual(list(channels)[0], channel)

        stored_events = dje.models.Event.objects.all()
        # 2 events seem to be created by the producer channel on welcome
        self.assertEqual(len(stored_events), 2)
        self.assertEqual(stored_events[1].type, "welcome")

    def test_get_channels_failure(self):
        pass

    def test_find_active_channels_success(self):
        pass

    def test_find_active_channels_no_producer(self):
        pass

    def test_find_active_channels_balance_producers(self):
        pass

    def test_check_consumer_inputs_success(self):
        pass

    def test_check_consumer_inputs_missing_data(self):
        pass

    def test_check_consumer_inputs_missing_model_wrong_task(self):
        pass

    def test_handle_query_request_success(self):
        pass

    def test_handle_query_request_no_producer(self):
        pass
