from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import unittest
from unittest.mock import patch
import json

import requests

from utils.mock_server import get_free_port, start_mock_server

PUG_BREED_INFO_ENDPOINT = "/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270"
PUG_FACTS_URL = "https://dogapi.dog/api/v2/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270"


class TestMockServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected_response_content = {
            "data": {
                "id": "a6ea38ed-f692-478e-af29-378d0e2cc270",
                "type": "breed",
                "attributes": {
                    "name": "Pug",
                    "description": "The Pug is a small, playful breed that is known for its comical expression, charming personality, and loyalty. This breed is native to China, where it was originally kept as a companion and lapdog by the imperial court.",
                    "life": {"max": 15, "min": 12},
                    "male_weight": {"max": 8, "min": 6},
                    "female_weight": {"max": 8, "min": 6},
                    "hypoallergenic": "false",
                },
                "relationships": {
                    "group": {
                        "data": {
                            "id": "f56dc4b1-ba1a-4454-8ce2-bd5d41404a0c",
                            "type": "group",
                        }
                    }
                },
            },
            "links": {
                "self": "https://dogapi.dog/api/v2/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270"
            },
        }

        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_request_response(self):
        port = self.mock_server_port
        mock_pug_facts_url = f"http://127.0.0.1:{port}" + PUG_BREED_INFO_ENDPOINT

        # Send a request to the mock API server and store the response.
        response = requests.get(mock_pug_facts_url)

        # Confirm that the request-response cycle completed successfully.
        self.assertEqual(
            response.status_code, 200, msg="Test for mock server 200 status code failed"
        )

        self.assertEqual(
            json.loads(response.content),
            self.expected_response_content,
            msg="Test for mock server content failed",
        )

    def test_mock_accuracy(self):
        """Test if the mock server response content matches the content from the real API"""

        port = self.mock_server_port
        mock_pug_facts_url = f"http://127.0.0.1:{port}" + PUG_BREED_INFO_ENDPOINT

        mock_server_response = requests.get(mock_pug_facts_url)
        mock_server_content = json.loads(mock_server_response.content)

        real_api_response = requests.get(PUG_FACTS_URL)
        real_api_content = json.loads(real_api_response.content)

        self.assertEqual(
            mock_server_content.keys(),
            real_api_content.keys(),
            msg="Test for mock accuracy failed",
        )
