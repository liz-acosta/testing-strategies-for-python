import unittest
import datetime
from unittest.mock import patch
from pug import Pug


class TestPug(unittest.TestCase):
    """Test Class for Class Pug"""
 
    def test_pug_instance_successful(self):
        """Tests if the instatiation of a class Pug is successful"""

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
        """Tests if the instatiation of a class Pug results in the correct exception"""
        
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


class TestPugWithSetup(unittest.TestCase):
    """Test Class for Class Pug with a pug class setup that occurs before all the tests"""

    @classmethod
    def setUpClass(cls):
        cls.test_pug = Pug("Gary", "14", "San Francisco", "5:00 PM")
    
    @patch('pug.openai.Image')
    def test_build_pug(self, mock_openai):

        mock_openai_response = {'data':[{'url': 'https://ai-generated-pug'}]}
        mock_openai.create.return_value = mock_openai_response
        
        expected_result = 'https://ai-generated-pug'
        test_result = self.test_pug.build_pug()
        self.assertEqual(test_result, expected_result, msg="Test for build_pug failed")


if __name__ == '__main__':
    unittest.main()
