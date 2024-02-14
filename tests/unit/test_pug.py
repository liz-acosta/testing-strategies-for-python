import unittest
import datetime
import requests
from unittest.mock import patch, Mock
from pug import Pug, get_pug_facts
from utils.mock_server import get_free_port, start_mock_server
import os

# Get TEST_ENV from environment variable
# Used below to determine tests to run or skip 
TEST_ENV = os.getenv("TEST_ENV", 'dev')

PUG_BREED_INFO_ENDPOINT = "/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270"

class TestPug(unittest.TestCase):
    """Test Class for Class Pug"""
 
    def test_pug_instance_successful(self):
        """Tests if the instance of a class Pug is successful"""

        test_result = Pug("Gary", "14", "San Francisco", "5:00 PM")
        test_data = [{'test_result': test_result.name,
                    'expected_result': "Gary",},
                    {'test_result': test_result.age,
                    'expected_result': 14,},
                    {'test_result': test_result.home,
                    'expected_result': "San Francisco",},
                    {'test_result': test_result.puppy_dinner,
                    'expected_result': "17:00"}]
        for data in test_data:
            self.assertEqual(data['test_result'], data['expected_result'])
    
    def test_pug_instance_exceptions(self):
        """Tests if the instance of a class Pug results in the correct exception"""
        
        test_data = [{'case': "Invalid age",
                      'name': "Gary",
                      'age': "fourteen",
                      'home': "San Francisco",
                      'puppy_dinner': "5:00 PM",
                      'expected_result': 
                      "Error creating PUG with name Gary: invalid literal for int() with base 10: 'fourteen'"
                      },
                      {'case': "Invalid puppy dinner",
                       'name': "Gary",
                       'age': "14",
                       'home': "San Francisco",
                       'puppy_dinner': "5:00",
                       'expected_result': 
                       "Error creating PUG with name Gary: time data '5:00' does not match format '%I:%M %p'"
                       }]
        for data in test_data:
            with self.subTest(msg=data['case']):
                with self.assertRaises(Exception) as test_e:
                    Pug(data['name'], data['age'], data['home'], data['puppy_dinner'])
                self.assertEqual(str(test_e.exception), data['expected_result'],
                msg="Test for pug instantiation exception failed")

    @patch('pug.requests')
    def test_get_pug_facts(self, mock_requests):

        mocked_pug_facts_response = Mock(requests.Response)
        mocked_pug_facts_response.content = b'{"data": {"id": "a6ea38ed-f692-478e-af29-378d0e2cc270", "type": "breed", "attributes": {"name": "Pug", "description": "The Pug is a small, playful breed that is known for its comical expression, charming personality, and loyalty. This breed is native to China, where it was originally kept as a companion and lapdog by the imperial court.", "life": {"max": 15, "min": 12}, "male_weight": {"max": 8, "min": 6}, "female_weight": {"max": 8, "min": 6}, "hypoallergenic": "false"}, "relationships": {"group": {"data": {"id": "f56dc4b1-ba1a-4454-8ce2-bd5d41404a0c", "type": "group"}}}}, "links": {"self": "https://dogapi.dog/api/v2/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270"}}'
        mock_requests.get.return_value = mocked_pug_facts_response

        expected_pug_facts = {
            'description': "The Pug is a small, playful breed that is known for its comical expression, charming personality, and loyalty. This breed is native to China, where it was originally kept as a companion and lapdog by the imperial court.",
            'max_age': 15,
            'weight': 18,
        }
        test_pug_facts = get_pug_facts()

        self.assertEqual(test_pug_facts, expected_pug_facts, msg="Test for get_pug_facts failed")


class TestPugWithSetup(unittest.TestCase):
    """Test Class for Class Pug with a pug class setup that occurs before all the tests"""

    @classmethod
    def setUpClass(cls):
        cls.test_pug = Pug("Gary", "14", "San Francisco", "5:00 PM")
    
    def test_pug_describe_pug(self):
        """Tests the describe_pug function"""

        expected_result = "Gary is a pug who is 14 years old and lives in San Francisco."
        test_result = self.test_pug.describe_pug()
        self.assertEqual(test_result, expected_result, msg="Test for describe_pug failed")
    
    @patch('pug.client.images')
    def test_build_pug(self, mock_openai):

        mock_openai_response = Mock()
        mock_openai_response.data = [Mock(url='https://ai-generated-pug')]
        mock_openai.generate.return_value = mock_openai_response
        
        expected_result = 'https://ai-generated-pug'
        test_result = self.test_pug.build_pug()
        self.assertEqual(test_result, expected_result, msg="Test for build_pug failed")
    
    @patch('pug.datetime')
    def test_check_for_puppy_dinner(self, mock_datetime):
        """Tests the check_for_puppy_dinner function"""
        
        test_data = [{'case': "Puppy dinner time",
                      'time': datetime.datetime(2023, 9, 21, 17, 00, 00, 000000),
                      'expected_result': "The current time is 05:00 PM. It is time for puppy dinner! 😍"},
                      {'case': "Not puppy dinner time",
                      'time': datetime.datetime(2023, 9, 21, 16, 00, 00, 000000),
                      'expected_result': 
                      "The current time is 04:00 PM. It is not yet time for puppy dinner 😔"}]
        for data in test_data:
            with self.subTest(msg=data['case']):
                mock_datetime.datetime.now.return_value = data['time']
                test_result = Pug.check_for_puppy_dinner(self.test_pug.puppy_dinner)
                self.assertEqual(test_result, data['expected_result'],
                msg="Test for check_for_puppy_dinner failed")

    def test_pug_drop_it(self):
        """Tests the drop_it function"""

        for i in range(5):
            self.test_pug.drop_it()

class TestPugFacts(unittest.TestCase):
    """Test Class to test the get_pug_facts function -- includes setup for a mock server for the Dog API `/breeds/{id}` endpoint"""
    @classmethod
    def setUpClass(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)
    
    @unittest.skipUnless(TEST_ENV.startswith('stage'), f"Skipping mock server test because TEST_ENV: {TEST_ENV}")
    def test_get_pug_facts_with_mock_server(self):
        """Tests get_puf_facts with call to mock API endpoint"""
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
