"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
      self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
      """It should return an error for duplicates"""
      result = self.client.post('/counters/bar')
      self.assertEqual(result.status_code, status.HTTP_201_CREATED)
      result = self.client.post('/counters/bar')
      self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        #1: Make a call to Create a counter.
        counter = self.client.post('/counters/test_counter')

        #2: Ensure that it returned a successful return code.
        self.assertEqual(counter.status_code, status.HTTP_201_CREATED)

        #3: Check the counter value as a baseline.
        counter_value = self.client.get('/counters/test_counter')
        self.assertEqual(counter_value.status_code, status.HTTP_200_OK)
        baseline = counter_value.json['test_counter']

        #4: Make a call to Update the counter that you just created.
        updated = self.client.put('/counters/test_counter')

        #5: Ensure that it returned a successful return code.
        self.assertEqual(updated.status_code, status.HTTP_200_OK)

        #6: Check that the counter value is one more than the baseline you measured in step 3.
        get_updated = self.client.get('/counters/test_counter')
        updated_value = get_updated.json['test_counter']
        self.assertEqual(updated_value, baseline + 1)

        nonexistent = self.client.put('/counters/nonexistent')
        self.assertEqual(nonexistent.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Counter nonexistent doesn't exist", nonexistent.json['Message'])

    def test_read_a_counter(self):
        """It should read a counter"""
        result = self.client.post('/counters/test_read_counter')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        read = self.client.get('/counters/test_read_counter')
        self.assertEqual(read.status_code, status.HTTP_200_OK)

        nonexistent = self.client.get('/counters/nonexistent')
        self.assertEqual(nonexistent.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Counter nonexistent doesn't exist", nonexistent.json['Message'])

