import unittest


class ExampleTestCaseClassTestFixtures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Class-level setup test fixture has been executed!")

    @classmethod
    def tearDownClass(cls):
        print("Class-level teardown test fixture has been executed!")

    def test_example_equal(self):
        self.assertEqual(1 + 1, 2)

    def test_example_not_equal(self):
        self.assertNotEqual(1 + 1, 3)


class ExampleTestCaseMethodTestFixtures(unittest.TestCase):

    def setUp(self):
        print("Method-level setup test fixture has been executed!")

    def tearDown(self):
        print("Method-level teardown test fixture has been executed!")

    def test_example_equal(self):
        self.assertEqual(1 + 1, 2)

    def test_example_not_equal(self):
        self.assertNotEqual(1 + 1, 3)
