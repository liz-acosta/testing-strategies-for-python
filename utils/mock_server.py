# Standard library imports...
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import socket
from threading import Thread
import unittest
import json

# Third-party imports...
import requests

DOG_BREED_INFO_RESPONSE = {
  "data": {
    "id": "a6ea38ed-f692-478e-af29-378d0e2cc270",
    "type": "breed",
    "attributes": {
      "name": "Pug",
      "description": "The Pug is a small, playful breed that is known for its comical expression, charming personality, and loyalty. This breed is native to China, where it was originally kept as a companion and lapdog by the imperial court.",
      "life": {
        "max": 15,
        "min": 12
      },
      "male_weight": {
        "max": 8,
        "min": 6
      },
      "female_weight": {
        "max": 8,
        "min": 6
      },
      "hypoallergenic": 'false'
    },
    "relationships": {
      "group": {
        "data": {
          "id": "f56dc4b1-ba1a-4454-8ce2-bd5d41404a0c",
          "type": "group"
        }
      }
    }
  },
  "links": {
    "self": "https://dogapi.dog/api/v2/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270"
  }
} 

class MockServerRequestHandler(BaseHTTPRequestHandler):
    USERS_PATTERN = re.compile(r'/breeds')

    def do_GET(self):
        if re.search(self.USERS_PATTERN, self.path):
            print("***** GET")
            # Add response status code.
            self.send_response(requests.codes.ok)

            # Add response headers.
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            # Add response content.
            response_content = json.dumps(DOG_BREED_INFO_RESPONSE)
            self.wfile.write(response_content.encode('utf-8'))
            return


def get_free_port():
    print("**** Got port")
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    print("*****", address, port)
    s.close()
    return port

def start_mock_server(port):
    print("**** Started mock server")
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    print("**** Started mock server 1")
    mock_server_thread = Thread(target=mock_server.serve_forever, daemon=True)
    print("**** Started mock server 2", mock_server_thread.is_alive)
    mock_server_thread.start()