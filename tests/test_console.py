import unittest
from unittest.mock import patch, Mock
from src.classes import database, console as csl


class TestConsole(unittest.TestCase):

    def setUp(self):
        # Set up a mock database for testing
        self.db = database.Database(host='test_host', user='test_user', passwd='test_password')
        self.db.mock_connection = Mock()
        self.console = csl.Console(db=self.db)

    def test_invalid_command_format(self):
        # Test when both -la and -ld switches are present
        with patch('builtins.input', side_effect=['l -la -ld']):
            with self.assertRaises(ValueError) as context:
                self.console.read_cmd('l -la -ld')
            self.assertEqual(str(context.exception), "-la and -ld switch cannot be used together")

        # Test when no parameter after -d switch
        with patch('builtins.input', side_effect=['l -d']):
            with self.assertRaises(ValueError) as context:
                self.console.read_cmd('l -d')
            self.assertEqual(str(context.exception), "Error - searching keyword missing after -d")

        # Test when regexes are not quoted
        with patch('builtins.input', side_effect=['l -t regex']):
            with self.assertRaises(ValueError) as context:
                self.console.read_cmd('l -t regex')
            self.assertEqual(str(context.exception), "Regular expression not quoted correctly: regex")

        # Test when regexes are corrupted
        with patch('builtins.input', side_effect=['l -t "unclosed regex']):
            with self.assertRaises(ValueError) as context:
                self.console.read_cmd('l -t "unclosed regex')
            self.assertEqual(str(context.exception), 'Regular expression not quoted correctly: "unclosed')


if __name__ == '__main__':
    unittest.main()