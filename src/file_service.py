import hashlib
import os


class FileService:
    @staticmethod
    def get_block_size(file_name):
        chunks_limit = 1500  # incoming request payload size are restricted to 100kb
        default_block_size = 4 * 1024 * 1024  # default chunk size of 4MB to get the most benefit out of deduplication

        file_size = os.path.getsize(file_name)

        if file_size / default_block_size > chunks_limit:
            return int(round(file_size / chunks_limit))
        else:
            return default_block_size

    @staticmethod
    def generate_etag(buf):
        sha1 = hashlib.sha1()
        sha1.update(buf)
        etag = sha1.hexdigest() + "-" + str(len(buf))

        return etag
