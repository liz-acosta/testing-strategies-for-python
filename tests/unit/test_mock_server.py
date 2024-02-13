# Standard library imports...
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import unittest
from unittest.mock import patch

# Third-party imports...
import requests

from utils.mock_server import get_free_port, start_mock_server
from pug import pug_facts

class TestMockServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_request_response(self):
        mock_pug_facts_url = 'http://127.0.0.1:{port}/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270'.format(port=self.mock_server_port)
    
        with patch.dict('pug.__dict__', {'PUG_FACTS_URL': mock_pug_facts_url}):
            expected_pug_facts = {
                'description': "The Pug is a small, playful breed that is known for its comical expression, charming personality, and loyalty. This breed is native to China, where it was originally kept as a companion and lapdog by the imperial court.",
                'max_age': 15,
                'weight': 18,
            }
            test_pug_facts = pug_facts()

            self.assertEqual(test_pug_facts, expected_pug_facts, msg="Test for pug_facts failed")
