from QREnv import QREnv

class QRStorageBucket:

    def __init__(self, name):
        self.name = name

    def get_info(self):
        if(QREnv.NO_PLATFORM):
            return True
        else:
            pass

    def get_file(self, bucket_file_path, save_to):
        pass

    def list(self):
        pass

    def rename(self, old_bucket_file_path, new_bucket_file_path):
        pass
    
    def create(self, bucket_file_path, local_file_path):
        pass