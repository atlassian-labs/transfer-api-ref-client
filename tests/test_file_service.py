import unittest
from unittest.mock import patch

from src.file_service import FileService


class TestClass(unittest.TestCase):

    @patch("os.path.getsize")
    def test_block_size_should_be_default(self, getsize):
        # mock
        getsize.return_value = 128
        default_block_size = 4 * 1024 * 1024

        block_size = FileService.get_block_size("test")

        self.assertEqual(default_block_size, block_size)

    @patch("os.path.getsize")
    def test_block_size_when_chunks_exceeded_limit(self, getsize):
        # mock
        getsize.return_value = 4 * 1024 * 1024 * 1024 * 1024
        default_block_size = 4 * 1024 * 1024

        block_size = FileService.get_block_size("test")

        self.assertNotEqual(default_block_size, block_size)

    def test_generate_etag(self):
        expected_etag = 'a17c9aaa61e80a1bf71d0d850af4e5baa9800bbd-4'

        actual_etag = FileService.generate_etag(b'data')

        self.assertEqual(expected_etag, actual_etag)


if __name__ == '__main__':
    unittest.main()
