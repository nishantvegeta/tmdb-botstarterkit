import os
import json
import requests
import urllib
import QRUtils
from urllib import request
from QREnv import QREnv
from storage_buckets.storage_bucket_exceptions import (
        BaseUrlNotSetException,
        ItemNotFoundException,
        IdentifierNotSetException,
        BucketNameNotSetException,
        BucketIdNotSetException,
        FileDownloadError
    )


class QRStorageBucket:

    bucket_id: int

    def __init__(self, bucket_type):
        """Base storage bucket name for which bot will work"""
        self._storage_bucket_name = None
        self.bucket_type = bucket_type

    def get_info(self):
        if(QREnv.NO_PLATFORM):
            return True
        else:
            pass

    @property
    def working_bucket(self):
        return self._storage_bucket_name

    @working_bucket.setter
    def set_working_bucket(self, bucket_name):
        self._storage_bucket_name = bucket_name

    @property
    def working_bucket_id(self):
        return self.bucket_id

    @working_bucket_id.setter
    def set_working_bucket_id(self, bucket_id):
        self.bucket_id = bucket_id

    def _get_base_url(self):
        if hasattr(QREnv,'BASE_URL'):
            base_url = QREnv.BASE_URL
            return base_url
        else:
            raise BaseUrlNotSetException

    def _gen_uri(self, is_bucket: bool=True, params:dict=None):
        """
        param is_bucket: True, generate uri for bucket information
        param is_bucket: False, generate uri for bucket data information
        """
        base_url = self._get_base_url()

        if is_bucket:
            path = f"bot/storagebuckets/"
            uri = urllib.parse.urljoin(base_url, path)
            
            """Not Implemented"""
            if params:
                pass
        else:
            # * Not implemented
            pass
        return uri

    def _gen_file_download_link(self, url):
        """Implemented for local"""
        base_url = self._get_base_url()
        uri = urllib.parse.urljoin(base_url, url)
        return uri

    @staticmethod
    def gen_headers():
        identifier = QREnv.IDENTIFIER
        if not identifier:
            raise IdentifierNotSetException

        return {
            "Accept":"application/json",
            "Authorization":f"identifier {identifier}"
        }
    
    def get_file(self, filename, bucket_type='Local', url=None, save_to=''):
        bucket_type = str(bucket_type).lower()

        if bucket_type == QREnv.STORAGE_LOCAL:
            download_link = self._gen_file_download_link(url=url)

        elif bucket_type == QREnv.STORAGE_S3:
            download_link = url

        filename = os.path.join(QREnv.DEFAULT_STORAGE_LOCATION, filename) if not save_to else os.path.join(save_to, filename)

        try:
            request.urlretrieve(url=download_link, filename=str(filename))
        except:
            raise FileDownloadError
        return True

    def post_file(self, filename, file_path):
        """Post file"""
        base_url = self._gen_uri()
        url_path = urllib.parse.urljoin(base_url, f"{self.bucket_id}/bucket_data/")

        file = {"file": open(file_path, "rb")}
        bucket_data_dictionary = {
            "file_display_name": filename
        }

        response = requests.post(
            url=url_path,
            headers=self.gen_headers(),
            data=bucket_data_dictionary,
            files=file
        )
        return response.json()


    def get_files_list(self, bucket_id=None):
        """If bucket id is already set, then no need to send bucket_id parameter"""
        if self.bucket_id:
            bucket_id = self.working_bucket_id
        else:
            if not bucket_id:
                raise Exception('BucketId not provided')
            self.set_working_bucket_id = bucket_id
        
        base_url = self._gen_uri()
        full_url = urllib.parse.urljoin(base_url, f'{self.working_bucket_id}/bucket_data')
        response = requests.get(
            url=full_url,
            headers=self.gen_headers()
            )
        files_list = response.json()
        QRUtils.display(files_list)
        return files_list

    def list_all_buckets(self):
        response = requests.get(
            url=self._gen_uri(),
            headers=self.gen_headers()
            )
        storage_buckets_list = response.json()
        return storage_buckets_list

    def get_working_bucket_info(self, bucket_name=None):
        """if working bucket is not set, provide bucket_name parameter"""

        if self.working_bucket != None:
            current_working_bucket = self.working_bucket
        else:
            QRUtils.display("I am here")
            # TODO: need to work on settar
            if bucket_name != None:
                current_working_bucket = self.set_working_bucket = bucket_name
            else:
                raise BucketNameNotSetException

        payload = {"bucket_name": current_working_bucket}
        response = requests.get(
                url=self._gen_uri(),
                headers=self.gen_headers(),
                params=payload
            )
        found_bucket = response.json()
        return found_bucket

    def rename(self, old_bucket_file_path, new_bucket_file_path):
        pass

    def copy_or_move(self, action, new_file_name):
        pass

    def create(self, bucket_file_path, local_file_path):
        pass