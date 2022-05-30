from django.test import Client, TestCase
from rest_framework.authtoken.models import Token
from channels.testing import ApplicationCommunicator

from feedapp.models import User, Cluster
from feedapp.tests import config


class ChannelManagerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            config.username, config.email, config.password
        )
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.cluster = self.create_cluster()
        self.headers = {"HTTP_AUTHORIZATION": f"Token {self.token}"}
        self.request_client = Client(**self.headers)

    def create_cluster(self, user=None):
        user = user if user else self.user
        new_cluster = Cluster(
            name=config.name, description=config.description, admin=user
        )
        new_cluster.save()
        new_cluster.members.add(user)
        new_cluster.save()

        return new_cluster

    def test_setup_http_consumer_connection_no_producer(self):
        r = self.request_client.post(
            f"/consumer/{self.token.key}/", data=config.get_query_data()
        )
        self.assertEqual(r.status_code, 418)

    def test_setup_http_producer_connection(self):
        r = self.request_client.post(f"/producer/{self.token.key}/")
        self.assertEqual(r.status_code, 200)
