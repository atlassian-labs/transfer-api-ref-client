import hashlib
import math


class FileService:
    @staticmethod
    def get_block_size(file_size):
        file_size_in_mb = file_size / (1024 * 1024)
        block_size = math.ceil(file_size_in_mb / 1000)
        if block_size < 5:
            block_size = 5
        elif block_size < 50:
            block_size = 50
        elif block_size < 100:
            block_size = 100
        else:
            block_size = 210
        return block_size * (1024 * 1024)

    @staticmethod
    def generate_etag(buf):
        sha256 = hashlib.sha256()
        sha256.update(buf)
        etag = sha256.hexdigest() + "-" + str(len(buf))

        return etag
