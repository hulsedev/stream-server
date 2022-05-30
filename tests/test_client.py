import unittest
import os

from hulse import Hulse


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get("MOCK_API_KEY")
        self.client = Hulse(api_key=self.api_key)

    def test_query_success(self):
        task = "text-classification"
        data = "I'm a little tea pot"
        result = self.client.query(task=task, data=data)
        print(result)
        self.assertEqual(type(result), dict)
        self.assertTrue("cluster" in result)
