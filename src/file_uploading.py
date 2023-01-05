import io
import itertools
import os
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from operator import itemgetter
from threading import Lock
from threading import BoundedSemaphore

import click
import requests
from colorama import init, Fore
from magic import from_file
from retrying import retry
from tqdm import tqdm

from src.custom_exceptions import AuthException
from src.file_service import FileService


class FileUploading:
    def __init__(self, file, issue_key, user, auth_token, base_url):
        self.file = file
        self.issue_key = issue_key
        self.user = user
        self.auth_token = auth_token
        self.base_url = base_url
        self.semaphore = BoundedSemaphore(8)

    def run(self):
        print(Fore.BLUE + "[Starting] ")
        init()
        auth = (self.user, self.auth_token)
        block_size = FileService.get_block_size(self.file)
        file_size = os.path.getsize(self.file)
        expected_chunks = (file_size // block_size) + 1
        lock = Lock()
        click.echo('Preparing file to upload: %s' % click.format_filename(self.file))
        t = tqdm(total=expected_chunks, unit='B', unit_scale=False)
        t.set_description("Uploading progress")
        count = itertools.count()
        upload_id = self.create_upload(self.base_url, auth, self.issue_key)
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                uploads = []
                with open(self.file, 'rb') as infile:
                    buf = infile.read(block_size)
                    while len(buf) > 0:
                        self.semaphore.acquire()
                        try:
                            future = executor.submit(self.process_chunk, self.base_url, auth, self.issue_key, buf, lock, t, count, upload_id)
                            uploads.append(future)
                            buf = infile.read(block_size)
                        except:
                            self.semaphore.release()
                            raise
                        else:
                            future.add_done_callback(lambda x: self.semaphore.release())
                chunk_list = [future.result() for future in futures.as_completed(uploads)]
            self.create_file_chunked(self.base_url, auth, chunk_list, self.file, self.issue_key, upload_id)
            t.update(1)
            t.close()
            click.echo('The file has been successfully uploaded and attached to the ticket %s' % self.issue_key)
        except AuthException as e:
            t.close()
            print(Fore.RED + "[ERROR] Authentication error. Check your API credentials.")   
            raise e         
        except Exception as e:
            print(Fore.RED + "[ERROR] " + str(e))
            raise e

    def process_chunk(self, base_url, auth, issue_key, buf, lock, progress, count, upload_id):
        index = next(count) + 1
        etag = FileService.generate_etag(buf)
        response = self.check_if_chunk_exists(base_url, auth, issue_key, [etag], upload_id)
        if not response["data"]["results"][etag]["exists"]:
            self.upload_chunk(base_url, auth, issue_key, etag, buf, upload_id, index)
        with lock:
            progress.update(1)
        return etag, index

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=5000, stop_max_attempt_number=5)
    def create_file_chunked(self, base_url, auth, chunk_list, file, issue_key, upload_id):
        chunk_list.sort(key=itemgetter(1))

        etagList = []
        for n in chunk_list:
            etagList.append(n[0])

        parameters = {'uploadId': upload_id}
        headers = {"Content-Type": "application/json"}
        response = requests.post(base_url + "/api/upload/" + issue_key + "/file/chunked",
                                 auth=auth,
                                 headers=headers,
                                 json={"chunks": self.__get_chunks_json(etagList),
                                       "name": os.path.basename(file),
                                       "mimeType": from_file(file, mime=True)}, params=parameters)
        self.__check_status_code(response.status_code)
        return response.json()

    @retry(wait_exponential_multiplier=100, wait_exponential_max=5000, stop_max_attempt_number=5)
    def check_if_chunk_exists(self, base_url, auth, issue_key, chunk_list, upload_id):
        headers = {"Content-Type": "application/json"}
        parameters = {'uploadId': upload_id}
        response = requests.post(base_url + "/api/upload/" + issue_key + "/chunk/probe",
                                 auth=auth,
                                 headers=headers,
                                 json={"chunks": self.__get_chunks_json(chunk_list)},
                                 params=parameters)
        self.__check_status_code(response.status_code)
        return response.json()

    @retry(wait_exponential_multiplier=100, wait_exponential_max=5000, stop_max_attempt_number=5)
    def upload_chunk(self, base_url, auth, issue_key, etag, buf, upload_id, part_number):
        parameters = {'uploadId': upload_id, 'partNumber': part_number}
        response = requests.post(base_url + "/api/upload/" + issue_key + "/chunk/" + etag,
                                 auth=auth,
                                 stream=True,
                                 files={"chunk": io.BytesIO(buf)}, params=parameters)
        self.__check_status_code(response.status_code)

    def create_upload(self, base_url, auth, issue_key):
        headers = {"Content-Type": "application/json"}
        response = requests.post(base_url + "/api/upload/" + issue_key,
                                 auth=auth,
                                 headers=headers)
        self.__check_status_code(response.status_code)
        return response.json()

    @staticmethod
    def __check_status_code(status_code):
        if status_code == 401:
            raise AuthException("Authentication required")
        if not (status_code == 200 or status_code == 201):
            raise Exception('Could not upload file, please try later again. status code: {0}'.format(status_code))

    @staticmethod
    def __get_chunks_json(chunk_list):
        chunks_json = []
        for val in chunk_list:
            etag = val.partition("-")
            chunks_json.append({"hash": etag[0], "size": etag[2]})

        return chunks_json
