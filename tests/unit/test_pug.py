import unittest
import datetime
import requests
from openai.types.images_response import ImagesResponse
from openai.types.image import Image
from unittest.mock import patch, MagicMock
from pug import Pug, get_pug_facts, PUG_FACTS_URL
from tests.utils.helpers import is_valid_url
import os

# Get TEST_ENV from environment variable
# Used below to determine tests to run or skip 
TEST_ENV = os.getenv("TEST_ENV", 'dev')

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

    # The following test uses the patch decorator to patch in a MagicMock object for the specified target
    # This test is also an example of using autospec=True to ensure that any attribute called on the mock
    # is an actual attribute of the mocked method
    # https://docs.python.org/3/library/unittest.mock.html#auto-speccing 
    @patch('pug.requests', autospec=True)
    def test_get_pug_facts(self, mock_requests):
        """Tests get_pug_facts with a mock requests object, checks if the correct URL is called"""
        
        mocked_pug_facts_response = MagicMock(spec=requests.Response)
        mock_requests.get.return_value = mocked_pug_facts_response

        expected_results = ['description', 'max_age', 'weight']
        test_results = get_pug_facts()
        
        self.assertEqual(expected_results, list(test_results.keys()))
        mock_requests.get.assert_called_with(PUG_FACTS_URL)

    # TODO: Uncomment the code below to see what happens when we don't use autospec
    # @patch('pug.requests')
    # def test_get_pug_facts_without_autospec(self, mock_requests):
    #     """Tests get_pug_facts with a mock requests object, checks if the correct URL is called"""
        
    #     mocked_pug_facts_response = MagicMock(spec=requests.Response)
    #     mock_requests.get_response.return_value = mocked_pug_facts_response
        
    #     expected_results = ['description', 'max_age', 'weight']
    #     test_results = get_pug_facts()
        
    #     self.assertEqual(expected_results, list(test_results.keys()))
    #     mock_requests.get_response.assert_called_with(PUG_FACTS_URL)
    
    # TODO: Uncomment the code below to see what happens when we don't use autospec
    # and try to call a method that does not exist for the Requests class
    # @patch('pug.requests', autospec=True)
    # def test_get_pug_facts_with_autospec_error(self, mock_requests):
    #     """Tests get_pug_facts with a mock requests object, checks if the correct URL is called"""
        
    #     mocked_pug_facts_response = MagicMock(spec=requests.Response)
    #     mock_requests.get_response.return_value = mocked_pug_facts_response
        
    #     expected_results = ['description', 'max_age', 'weight']
    #     test_results = get_pug_facts()
        
    #     self.assertEqual(expected_results, list(test_results.keys()))
    #     mock_requests.get.assert_called_with(PUG_FACTS_URL)
        
    #     self.assertEqual(expected_results, list(test_results.keys()))
    #     mock_requests.get_response.assert_called_with(PUG_FACTS_URL)

    @unittest.skipUnless(TEST_ENV.startswith('prod'), f"Skipping real API test because TEST_ENV: {TEST_ENV}")
    def test_get_pug_facts_with_real_api_call(self):
        """Tests get_pug_facts with call to real API endpoint, checks the returned json for the keys used in the method"""
        
        expected_result = ['description', 'max_age', 'weight']
        test_result = get_pug_facts()

        self.assertEqual(list(test_result.keys()), expected_result, msg="Test for get_pug_facts with real API call failed")

class TestPugWithSetup(unittest.TestCase):
    """Test Class for Class Pug with a pug class setup that occurs before all the tests"""

    @classmethod
    def setUpClass(cls):
        cls.test_pug = Pug("Gary", "14", "San Francisco", "5:00 PM")
    
    def test_pug_describe_pug(self):
        """Tests describe_pug"""

        expected_result = "Gary is a pug who is 14 years old and lives in San Francisco."
        test_result = self.test_pug.describe_pug()
        self.assertEqual(test_result, expected_result, msg="Test for describe_pug failed")
    
    # The following test uses assert_called_with() to verify the mock was called correctly 
    @patch('pug.client.images', autospec=True)
    def test_build_pug(self, mock_openai):
        """Tests build_pug using mock OpenAI client, checks if the correct arguments are used"""

        pug_description = self.test_pug.describe_pug()

        expected_arguments = {
            'prompt': f"A cute photo of {self.test_pug.name}. {pug_description}.",
            'n': 1,
            'size': "1024x1024"}

        mock_openai_response = ImagesResponse(created=1234,
                                              data=[Image(b64_json=None,
                                                          revised_prompt=None,
                                                          url="https://ai-generated-pug")])

        mock_openai.generate.return_value = mock_openai_response
        
        test_result = self.test_pug.build_pug()
        
        self.assertIs(str, type(test_result)) 
        mock_openai.generate.assert_called_with(
            prompt=expected_arguments['prompt'],
            n=expected_arguments['n'],
            size=expected_arguments['size'])

    @unittest.skipUnless(TEST_ENV.startswith('prod'), f"Skipping real API test because TEST_ENV: {TEST_ENV}")
    def test_build_pug_with_real_openai_client(self):
        """Tests the check_for_puppy_dinner function"""

        test_result = self.test_pug.build_pug()
        self.assertTrue(is_valid_url(test_result), msg="Test for build_pug with real OpenAI client failed")
    
    @patch('pug.datetime', autospec=True)
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
                mock_datetime.now.return_value = data['time']
                test_result = Pug.check_for_puppy_dinner(self.test_pug.puppy_dinner)
                self.assertEqual(test_result, data['expected_result'],
                msg="Test for check_for_puppy_dinner failed")

    # TODO: Uncomment the code below to see what happens when we patch the wrong target  
    # @patch('datetime.datetime', autospec=True)
    # def test_check_for_puppy_dinner_wrong_target(self, mock_datetime):
    #     """Tests the check_for_puppy_dinner function"""
        
    #     test_data = [{'case': "Puppy dinner time",
    #                   'time': datetime.datetime(2023, 9, 21, 17, 00, 00, 000000),
    #                   'expected_result': "The current time is 05:00 PM. It is time for puppy dinner! 😍"},
    #                   {'case': "Not puppy dinner time",
    #                   'time': datetime.datetime(2023, 9, 21, 16, 00, 00, 000000),
    #                   'expected_result': 
    #                   "The current time is 04:00 PM. It is not yet time for puppy dinner 😔"}]
    #     for data in test_data:
    #         with self.subTest(msg=data['case']):
    #             mock_datetime.now.return_value = data['time']
    #             test_result = Pug.check_for_puppy_dinner(self.test_pug.puppy_dinner)
    #             self.assertEqual(test_result, data['expected_result'],
    #             msg="Test for check_for_puppy_dinner failed")

if __name__ == '__main__':
    unittest.main()
