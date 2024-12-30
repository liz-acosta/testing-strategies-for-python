import unittest
import datetime
import requests
import sqlite3
from openai.types.images_response import ImagesResponse
from openai.types.image import Image
from unittest.mock import patch, MagicMock
from build_a_pug.pug import Pug, PugDB, get_pug_facts, PUG_FACTS_URL
from tests.utils.helpers import is_valid_url

from dotenv import load_dotenv
from colorama import init, Fore
import os

load_dotenv()
init(autoreset=True)

# Get TEST_ENV from environment variable
# Used below to determine tests to run or skip
TEST_ENV = os.getenv("TEST_ENV", "dev")
TEST_DATABASE_FILEPATH = "tests/test_db.sqlite"


class TestPug(unittest.TestCase):
    """Test Class for Class Pug"""

    def test_pug_instance_successful(self):
        """Tests if the instance of a class Pug is successful"""

        test_result = Pug("Gary", "14", "San Francisco", "5:00 PM")
        test_data = [
            {
                "test_result": test_result.name,
                "expected_result": "Gary",
            },
            {
                "test_result": test_result.age,
                "expected_result": 14,
            },
            {
                "test_result": test_result.home,
                "expected_result": "San Francisco",
            },
            {"test_result": test_result.puppy_dinner, "expected_result": "17:00"},
        ]
        for data in test_data:
            self.assertEqual(data["test_result"], data["expected_result"])

    def test_pug_instance_exceptions(self):
        """Tests if the instance of a class Pug results in the correct exception"""

        test_data = [
            {
                "case": "Invalid age",
                "name": "Gary",
                "age": "fourteen",
                "home": "San Francisco",
                "puppy_dinner": "5:00 PM",
                "expected_result": "Error creating PUG with name Gary: invalid literal for int() with base 10: 'fourteen'",
            },
            {
                "case": "Invalid puppy dinner",
                "name": "Gary",
                "age": "14",
                "home": "San Francisco",
                "puppy_dinner": "5:00",
                "expected_result": "Error creating PUG with name Gary: time data '5:00' does not match format '%I:%M %p'",
            },
        ]
        for data in test_data:
            with self.subTest(msg=data["case"]):
                with self.assertRaises(Exception) as test_e:
                    Pug(data["name"], data["age"], data["home"], data["puppy_dinner"])
                self.assertEqual(
                    str(test_e.exception),
                    data["expected_result"],
                    msg="Test for pug instantiation exception failed",
                )

    # The following test uses the patch decorator to patch in a MagicMock object for the specified target
    # This test is also an example of using autospec=True to ensure that any attribute called on the mock
    # is an actual attribute of the mocked method
    # https://docs.python.org/3/library/unittest.mock.html#auto-speccing
    @patch("build_a_pug.pug.requests", autospec=True)
    def test_get_pug_facts(self, mock_requests):
        """Tests get_pug_facts with a mock requests object, checks if the correct URL is called"""

        mocked_pug_facts_response = MagicMock(spec=requests.Response)
        mock_requests.get.return_value = mocked_pug_facts_response

        expected_results = ["description", "max_age", "weight"]
        test_results = get_pug_facts()

        self.assertEqual(expected_results, list(test_results.keys()))
        mock_requests.get.assert_called_with(PUG_FACTS_URL)

    @unittest.skipUnless(
        TEST_ENV.startswith("prod"),
        f"Skipping real API test because TEST_ENV: {TEST_ENV}",
    )
    def test_get_pug_facts_with_real_api_call(self):
        """Tests get_pug_facts with call to real API endpoint, checks the returned json for the keys used in the method"""

        expected_result = ["description", "max_age", "weight"]
        test_result = get_pug_facts()

        self.assertEqual(
            list(test_result.keys()),
            expected_result,
            msg="Test for get_pug_facts with real API call failed",
        )


class TestPugWithSetup(unittest.TestCase):
    """Test Class for Class Pug with a pug class setup that occurs before all the tests"""

    @classmethod
    def setUpClass(cls):
        cls.test_pug = Pug("Gary", "14", "San Francisco", "5:00 PM")

    def test_pug_describe_pug(self):
        """Tests describe_pug"""

        expected_result = (
            "Gary is a pug who is 14 years old and lives in San Francisco."
        )
        test_result = self.test_pug.describe_pug()
        self.assertEqual(
            test_result, expected_result, msg="Test for describe_pug failed"
        )

    # The following test uses assert_called_with() to verify the mock was called correctly
    @patch("build_a_pug.pug.client.images", autospec=True)
    def test_build_pug(self, mock_openai):
        """Tests build_pug using mock OpenAI client, checks if the correct arguments are used"""

        pug_description = self.test_pug.describe_pug()

        expected_arguments = {
            "prompt": f"A cute photo of {self.test_pug.name}. {pug_description}.",
            "n": 1,
            "size": "1024x1024",
        }

        mock_openai_response = ImagesResponse(
            created=1234,
            data=[
                Image(
                    b64_json=None, revised_prompt=None, url="https://ai-generated-pug"
                )
            ],
        )

        mock_openai.generate.return_value = mock_openai_response

        test_result = self.test_pug.build_pug()

        self.assertIs(str, type(test_result))
        mock_openai.generate.assert_called_with(
            prompt=expected_arguments["prompt"],
            n=expected_arguments["n"],
            size=expected_arguments["size"],
        )

    @unittest.skipUnless(
        TEST_ENV.startswith("prod"),
        f"Skipping real API test because TEST_ENV: {TEST_ENV}",
    )
    def test_build_pug_with_real_openai_client(self):
        """Tests the check_for_puppy_dinner function"""

        test_result = self.test_pug.build_pug()
        self.assertTrue(
            is_valid_url(test_result),
            msg="Test for build_pug with real OpenAI client failed",
        )

    @patch("build_a_pug.pug.datetime", autospec=True)
    def test_check_for_puppy_dinner(self, mock_datetime):
        """Tests the check_for_puppy_dinner function"""

        test_data = [
            {
                "case": "Puppy dinner time",
                "time": datetime.datetime(2023, 9, 21, 17, 00, 00, 000000),
                "expected_result": "The current time is 05:00 PM. It is time for puppy dinner! 😍",
            },
            {
                "case": "Not puppy dinner time",
                "time": datetime.datetime(2023, 9, 21, 16, 00, 00, 000000),
                "expected_result": "The current time is 04:00 PM. It is not yet time for puppy dinner 😔",
            },
        ]
        for data in test_data:
            with self.subTest(msg=data["case"]):
                mock_datetime.now.return_value = data["time"]
                test_result = Pug.check_for_puppy_dinner(self.test_pug.puppy_dinner)
                self.assertEqual(
                    test_result,
                    data["expected_result"],
                    msg="Test for check_for_puppy_dinner failed",
                )


class TestPugDB(unittest.TestCase):
    """Test class for tests related to the pug database"""

    def setUp(self):
        """Create a test database before every test method in this class"""

        self.connection = sqlite3.connect(TEST_DATABASE_FILEPATH)
        self.connection.row_factory = (
            sqlite3.Row
        )  # Optional: Access rows as dictionaries
        self.cursor = self.connection.cursor()

        test_pug_lily = Pug("Lily", "6", "San Francisco", "4:00 PM")
        test_pug_lily.description = "Lily is the best pug"
        test_pug_lily.image = "lily_pug.jpg"

        test_pug_fiona = Pug("Fiona", "2", "San Francisco", "4:00 PM")
        test_pug_fiona.description = "Fiona is the best pug"
        test_pug_fiona.image = "sweet_fiona.jpg"

        test_pugs = [test_pug_lily, test_pug_fiona]

        with open("build_a_pug/schema.sql", "r") as f:
            self.connection.executescript(f.read())

        query = "INSERT INTO pug (name, age, home, puppy_dinner, description, image) VALUES (?, ?, ?, ?, ?, ?)"
        for pug in test_pugs:
            self.connection.execute(
                query,
                (
                    pug.name,
                    pug.age,
                    pug.home,
                    pug.puppy_dinner,
                    pug.description,
                    pug.image,
                ),
            )

            self.connection.commit()

        print(
            Fore.GREEN
            + f"Test database: {TEST_DATABASE_FILEPATH} connection created and test data inserted"
        )

    def tearDown(self):
        """Close and delete the test database before after test method in this class"""

        self.connection.close()
        os.remove(TEST_DATABASE_FILEPATH)
        print(
            Fore.RED
            + f"Test database: {TEST_DATABASE_FILEPATH} connection closed and deleted"
        )

    def test_create_pug(self):
        """Test to see if a pug row is successfully created in the database"""

        test_pug = Pug("Gary", "14", "San Francisco", "5:00 PM")
        test_pug.description = "Gary is the best pug."
        test_pug.image = "cute_pug.jpg"

        test_db = self.connection

        PugDB.create_pug(test_db, test_pug)

        test_results = self.cursor.execute(
            "SELECT * FROM pug WHERE NAME = 'Gary'"
        ).fetchone()

        self.assertEqual(test_results["name"], "Gary")

    def test_create_pug_with_exception(self):
        """Test to see if an IntegrityError is raised when attempting to create an existing pug"""

        test_pug = Pug("Lily", "14", "San Francisco", "5:00 PM")
        test_pug.description = "Lily is the cutest pug."
        test_pug.image = "cute_pug.jpg"

        test_db = self.connection

        with self.assertRaises(Exception) as test_e:
            PugDB.create_pug(test_db, test_pug)
            self.assertEqual(type(test_e), self.connection.IntegrityError)

    def test_get_grumble(self):
        """Test to see if all the pugs are retrieved from the database"""

        test_db = self.connection
        test_results = PugDB.get_grumble(test_db)
        test_results = self.cursor.execute("SELECT * FROM pug").fetchall()
        self.assertEqual(len(test_results), 2)


if __name__ == "__main__":
    unittest.main()
