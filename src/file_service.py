import hashlib
import os


class FileService:
    @staticmethod
    def get_block_size(file_name):
        default_block_size = 10 * 1024 * 1024  # default chunk size of 4MB to get the most benefit out of deduplication

        return default_block_size

    @staticmethod
    def generate_etag(buf):
        sha1 = hashlib.sha1()
        sha1.update(buf)
        etag = sha1.hexdigest() + "-" + str(len(buf))

        return etag
