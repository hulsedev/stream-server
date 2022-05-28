import unittest
import os


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get("MOCK_API_KEY")

    def test_query_success(self):
        pass
