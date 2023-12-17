import unittest
from unittest.mock import patch, Mock
from src.classes import database, console


class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Set up a mock database connection for testing
        self.db = database.Database(host='test_host', user='test_user', passwd='test_password')
        self.db.connection = Mock()
        # self.db.connect()

    def tearDown(self):
        # Clean up after each test
        self.db.close()

    def test_get_movie_data(self):
        mock_cursor = self.db.connection.cursor.return_value
        mock_cursor.fetchall.return_value = [(1, 'Movie1', 'Director1', 2022, 120)]

        movies = self.db.get_movie_data()
        # Assert the expected result based on the mocked data
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0].title, 'Movie1')
        self.assertEqual(movies[0].director_name, 'Director1')
        self.assertEqual(movies[0].release_year, 2022)
        self.assertEqual(movies[0].length_minutes, 120)

    # Add more test cases for other Database methods...


if __name__ == '__main__':
    unittest.main()