import unittest

from src.file_service import FileService


class TestClass(unittest.TestCase):
    MB_TO_BYTES_MULTIPLIER = 1 * 1024 * 1024
    GB_TO_BYTES_MULTIPLIER = 1 * 1024 * MB_TO_BYTES_MULTIPLIER
    TB_TO_BYTES_MULTIPLIER = 1 * 1024 * GB_TO_BYTES_MULTIPLIER

    def test_generate_etag(self):
        expected_etag = '3a6eb0790f39ac87c94f3856b2dd2c5d110e6811602261a9a923d3bb23adc8b7-4'

        actual_etag = FileService.generate_etag(b'data')

        self.assertEqual(expected_etag, actual_etag)

    def test_default_block_size(self):
        file_size_byte = 2 * self.MB_TO_BYTES_MULTIPLIER
        expected_block_size_byte = 5 * self.MB_TO_BYTES_MULTIPLIER

        actual_block_size_byte = FileService.get_block_size(file_size_byte)

        self.assertEqual(expected_block_size_byte, actual_block_size_byte)

    def test_block_size_less_than_50_gb_file(self):
        file_size_byte = 50 * self.GB_TO_BYTES_MULTIPLIER
        expected_block_size_byte = 50 * self.MB_TO_BYTES_MULTIPLIER

        actual_block_size_byte = FileService.get_block_size(file_size_byte)

        self.assertEqual(expected_block_size_byte, actual_block_size_byte)

    def test_block_size_less_than_950_gb_file(self):
        file_size_byte = 960 * self.GB_TO_BYTES_MULTIPLIER
        expected_block_size_byte = 100 * self.MB_TO_BYTES_MULTIPLIER

        actual_block_size_byte = FileService.get_block_size(file_size_byte)

        self.assertEqual(expected_block_size_byte, actual_block_size_byte)

    def test_block_size_less_than_2_tb_file(self):
        file_size_byte = 2 * self.TB_TO_BYTES_MULTIPLIER
        expected_block_size_byte = 210 * self.MB_TO_BYTES_MULTIPLIER

        actual_block_size_byte = FileService.get_block_size(file_size_byte)

        self.assertEqual(expected_block_size_byte, actual_block_size_byte)


if __name__ == '__main__':
    unittest.main()
