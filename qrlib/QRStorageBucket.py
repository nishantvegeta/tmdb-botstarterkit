import re
import os
import json
import requests
import urllib
import QRUtils
from urllib import request
from qrlib.QREnv import QREnv
from storage_buckets.storage_bucket_exceptions import (
        BaseUrlNotSetException,
        IdentifierNotSetException,
        BucketNameNotSetException,
        BucketIdNotSetException,
        FileDownloadError
    )


class QRStorageBucket:
    """
    Storage bucket bot library.
    After object creation:
    Call get_and_set_working_bucket_info methods to initialize working bucket information
    """
    
    def __init__(self):
        """Base storage bucket name for which bot will work"""
        self._working_storage_bucket = None
        self._working_bucket_type = self._working_bucket_id = None

    def get_info(self):
        if(QREnv.NO_PLATFORM):
            return True
        else:
            pass

    @property
    def working_bucket(self):
        return self._working_storage_bucket

    @working_bucket.setter
    def set_working_bucket(self, bucket_name):
        self._working_storage_bucket = bucket_name

    @property
    def working_bucket_id(self):
        return self._working_bucket_id

    @working_bucket_id.setter
    def set_working_bucket_id(self, bucket_id):
        self._working_bucket_id = bucket_id

    @property
    def working_bucket_type(self):
        return self._working_bucket_type

    @working_bucket_type.setter
    def set_working_bucket_type(self, bucket_type):
        self._working_bucket_type = bucket_type

    # * URI Generation Methods
    @staticmethod
    def gen_headers():
        identifier = QREnv.IDENTIFIER
        if not identifier:
            raise IdentifierNotSetException

        return {
                "Accept":"application/json",
                "Authorization":f"identifier {identifier}"
            }
    
    @staticmethod
    def _base_url():
        if hasattr(QREnv, 'BASE_URL'):
            base_url = QREnv.BASE_URL
            return base_url
        else:
            raise BaseUrlNotSetException

    def _gen_api_base_uri(self, is_bucket: bool=True, params: dict=None):
        """
        param is_bucket: True, generate uri for working bucket information
        param is_bucket: False, generate uri for working bucket data information
        """
        base_url = self._base_url()
        path = f"bot/storagebuckets/"

        if not is_bucket:
            # * base url for bucket data
            bucket_id = getattr(self, "_working_bucket_id", None)
            if bucket_id is None:
                raise BucketIdNotSetException
            path = f"{path}{bucket_id}/bucket_data/"

        uri = urllib.parse.urljoin(base_url, path)
        return uri
        
    def _gen_file_download_link(self, file_url):
        """Implemented for local storage for file downloads"""
        base_url = self._base_url()
        uri = urllib.parse.urljoin(base_url, file_url)
        return uri
    
    # * Bucket Processing Methods
    def set_working_bucket_info(self, bucket_info: dict):
        self.set_working_bucket_id = bucket_info.get('id')
        self.set_working_bucket = bucket_info.get('bucket_name')
        self.set_working_bucket_type = bucket_info.get('bucket_type')

    def list_all_buckets(self):
        response = requests.get(
            url=self._gen_api_base_uri(),
            headers=self.gen_headers()
            )
        storage_buckets_list = response.json()
        return storage_buckets_list

    def get_and_set_working_bucket_info(self, bucket_name=None):
        """
        Validate working bucket name and set necessary information
        """
        if bucket_name != None:
            current_working_bucket = bucket_name
        else:
            raise BucketNameNotSetException
            
        payload = {"bucket_name": current_working_bucket}
        response = requests.get(
                    url=self._gen_api_base_uri(),
                    headers=self.gen_headers(),
                    params=payload
                )
        found_bucket = response.json()

        if found_bucket:
            self.set_working_bucket_info(bucket_info=found_bucket[0])
        return found_bucket

    # * File Processing Methods
    def download_file(self, file_item: dict, save_to_folder=''):
        bucket_type = str(self.working_bucket_type).lower()
        file_url = file_item.get('file')
        
        filename_str = str(file_item.get('file_display_name'))
        regex_filename = re.findall(r"(([^/]+/)*)([\w._]+)+", string=filename_str)[0]
        filename = str(regex_filename[2]).split(".")

        filename = filename[1] if not filename[0] else filename[0]
        
        if bucket_type == QREnv.STORAGE_LOCAL:
            download_link = self._gen_file_download_link(file_url=file_url)

        elif bucket_type == QREnv.STORAGE_S3:
            download_link = file_url

        with requests.get(download_link) as response:
            response.raise_for_status()
            extension = response.headers['Content-Type'].split('/')[-1]
            full_file_name = f"{filename}.{extension}"
            filename = os.path.join(QREnv.DEFAULT_STORAGE_LOCATION, full_file_name) if not save_to_folder else os.path.join(save_to_folder, full_file_name)
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        return full_file_name

    def post_file(self, filename, file_path):
        base_url = self._gen_api_base_uri(is_bucket=False)

        file = {"file": open(file_path, "rb")}
        bucket_data_dictionary = {
            "file_display_name": filename
        }

        response = requests.post(
            url=base_url,
            headers=self.gen_headers(),
            data=bucket_data_dictionary,
            files=file
        )
        return response.json()

    def list_all_files(self):
        base_url = self._gen_api_base_uri(is_bucket=False)
        response = requests.get(
            url=base_url,
            headers=self.gen_headers()
            )
        files_list = response.json()
        return files_list

    def search_and_get_file(self, find_filename: str):
        base_url = self._gen_api_base_uri(is_bucket=False)
        file_search_url = urllib.parse.urljoin(base_url, f'?file_name={find_filename}')

        response = requests.get(
            url=file_search_url,
            headers=self.gen_headers()
            )
        files_list = response.json()

        return files_list
    
    def file_operation(self, action: str, file_obj_id: int, new_file_name: str):
        base_url = self._gen_api_base_uri(is_bucket=False)
        full_url = urllib.parse.urljoin(base_url, f'{file_obj_id}/')
        data = {
                "file_display_name": new_file_name,
                "action": action
            }
        response = requests.patch(url=full_url, headers=self.gen_headers(), data=data)
        QRUtils.display(response.json())
        return response
