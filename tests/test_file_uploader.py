import random
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from app import command
from tests.utils.mock_response import mocked_request_500, mocked_request, mocked_request_401


@patch("builtins.open")
@patch("os.path.getsize")
class TestMain(unittest.TestCase):
    cli_args = ["--file=test", "--issue_key=DATA-777", "--user=bob", "--auth_token=builder"]

    def setUp(self):
        self.runner = CliRunner()

    @patch("requests.post", side_effect=mocked_request)
    def test_successfully_uploaded_file(self, mock_file, getsize, requests_post):
        # mock
        getsize.return_value = random.randint(128, 8192)

        # run
        result = self.runner.invoke(command, args=self.cli_args)
        self.assertTrue(not result.exception)
        self.assertEqual(0, result.exit_code)

    @patch("requests.post", side_effect=mocked_request_401)
    def test_unauthorized(self, mock_file, getsize, requests_post):
        # mock
        getsize.return_value = random.randint(128, 8192)

        # run
        result = self.runner.invoke(command, args=self.cli_args)
        self.assertEqual(result.exception.args[0], "Authentication required")
        self.assertEqual(1, result.exit_code)

    @patch("requests.post", side_effect=mocked_request_500)
    def test_retries(self, mock_file, getsize, requests_post):
        # mock
        getsize.return_value = random.randint(128, 8192)

        # run
        result = self.runner.invoke(command, args=self.cli_args)

        self.assertEqual(requests_post.call_count, 6)
        self.assertEqual(result.exception.args[0], "Could not upload file, please try later again. status code: 500")
        self.assertEqual(1, result.exit_code)


if __name__ == '__main__':
    unittest.main()
