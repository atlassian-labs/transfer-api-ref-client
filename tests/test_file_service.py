import unittest
from unittest.mock import patch

from src.file_service import FileService


class TestClass(unittest.TestCase):

    def test_generate_etag(self):
        expected_etag = 'a17c9aaa61e80a1bf71d0d850af4e5baa9800bbd-4'

        actual_etag = FileService.generate_etag(b'data')

        self.assertEqual(expected_etag, actual_etag)


if __name__ == '__main__':
    unittest.main()
