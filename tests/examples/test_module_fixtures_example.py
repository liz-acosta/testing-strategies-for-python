import unittest


def setUpModule():
    print("Module-level setup test fixture has been executed!")


def tearDownModule():
    print("Module-level teardown test fixture has been executed!")


class ExampleTestCaseSecond(unittest.TestCase):

    def test_example_equal(self):
        self.assertEqual(1 + 1, 2)

    def test_example_not_equal(self):
        self.assertNotEqual(1 + 1, 3)


class ExampleTestCaseFirst(unittest.TestCase):

    def test_example_equal(self):
        self.assertEqual(1 + 1, 2)

    def test_example_not_equal(self):
        self.assertNotEqual(1 + 1, 3)
