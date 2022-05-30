from django.test import Client, TestCase
from rest_framework.authtoken.models import Token
from channels.testing import ApplicationCommunicator

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

    def create_cluster(self, user=None):
        user = user if user else self.user
        new_cluster = Cluster(
            name=config.name, description=config.description, admin=user
        )
        new_cluster.save()
        new_cluster.members.add(user)
        new_cluster.save()

        return new_cluster

    def test_read_channel_success(self):
        pass

    def test_read_channel_failure(self):
        pass

    def test_get_channels_success(self):
        pass

    def test_get_channels_failure(self):
        pass
