from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item_tt, run_item_tf
from qrlib.QRStorageBucket import QRStorageBucket
from DefaultComponent import DefaultComponent
from RPA.Browser.Selenium import Selenium
from qrlib import QRUtils

class DefaultProcess(QRProcess):
    
    def __init__(self):
        super().__init__()
        """
        _subscriber=set
        def register
        def unregister
        def notify
        #
        run_item
        """

        self.default_component = DefaultComponent(self)
        self.data = []


    @run_item_tt()
    def execute_run_item(self, *args, **kwargs):
        self.default_component.test()

    # @run_item_tf()
    def before_run(self, *args, **kwargs):  
        #self.default_component.login()
        # queue_items = self.default_component.get_queue_items()
        # self.default_component.change_queue_items(queue_items)
        # self.data = ["a","b"]
        bucket = QRStorageBucket()
        # QRUtils.display(bucket.list_all_buckets())
        bucket.get_and_set_working_bucket_info(bucket_name='testing')
        file_list = bucket.list_all_files()
        QRUtils.display(file_list)
        QRUtils.display(file_list[6])
        download = bucket.download_file(file_item=file_list[5])
        QRUtils.display(download)
        # QRUtils.display(bucket.search_and_get_file(find_filename="bhuwna_.png_"))

    @run_item_tf()
    def after_run(self, *args, **kwargs):
        self.default_component.logout()
    
    @run_item_tf()
    def before_run_item(self, *args, **kwargs):
        self.run_item.logger.info(f"In pre run item = {args[0]}")

    @run_item_tf()
    def after_run_item(self, *args, **kwargs):
        self.run_item.logger.info(f"In post run item = {args[0]}")

    def run(self):
        for item in self.data:
            self.before_run_item(item)
            self.execute_run_item(item)
            self.after_run_item(item)


