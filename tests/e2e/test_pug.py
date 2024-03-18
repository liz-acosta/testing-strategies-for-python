import unittest
import datetime
import requests
from unittest.mock import patch, Mock
from pug import Pug, get_pug_facts
from utils.mock_server import get_free_port, start_mock_server
import os

# Get TEST_ENV from environment variable
# Used below to determine tests to run or skip 
TEST_ENV = os.getenv("TEST_ENV", 'stage')

PUG_BREED_INFO_ENDPOINT = "/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270"

class TestPugFacts(unittest.TestCase):
    """Test Class to test the get_pug_facts function -- includes setup for a mock server for the Dog API `/breeds/{id}` endpoint"""
    @classmethod
    def setUpClass(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)
    
    @unittest.skipUnless(TEST_ENV.startswith('stage'), f"Skipping mock server test because TEST_ENV: {TEST_ENV}")
    def test_get_pug_facts_with_mock_server(self):
        """Tests get_pug_facts with call to mock API endpoint"""
        port = self.mock_server_port
        mock_pug_facts_url = f'http://127.0.0.1:{port}' + PUG_BREED_INFO_ENDPOINT
    
        # Patch the pug facts URL dict object with the mock pug facts URL derived from the mock server
        with patch.dict('pug.__dict__', {'PUG_FACTS_URL': mock_pug_facts_url}):
            expected_pug_facts = {
                'description': "The Pug is a small, playful breed that is known for its comical expression, charming personality, and loyalty. This breed is native to China, where it was originally kept as a companion and lapdog by the imperial court.",
                'max_age': 15,
                'weight': 18,
            }
            test_pug_facts = get_pug_facts()

            self.assertEqual(test_pug_facts, expected_pug_facts, msg="Test for get_pug_facts with mock server failed")

    @unittest.skipUnless(TEST_ENV.startswith('prod'), f"Skipping real API test because TEST_ENV: {TEST_ENV}")
    def test_get_pug_facts_with_real_api_call(self):
        """Tests get_puf_facts with call to real API endpoint"""
        expected_pug_facts = {
            'description': "The Pug is a small, playful breed that is known for its comical expression, charming personality, and loyalty. This breed is native to China, where it was originally kept as a companion and lapdog by the imperial court.",
            'max_age': 15,
            'weight': 18,
        }
        test_pug_facts = get_pug_facts()

        self.assertEqual(test_pug_facts, expected_pug_facts, msg="Test for get_pug_facts with real API call failed")


if __name__ == '__main__':
    unittest.main()
