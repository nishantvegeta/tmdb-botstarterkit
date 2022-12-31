from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item_tt, run_item_tf
from qrlib.QRStorageBucket import QRStorageBucket
from DefaultComponent import DefaultComponent
from RPA.Browser.Selenium import Selenium


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
        bucket = QRStorageBucket(bucket_type='S3')
        bucket_info = bucket.get_working_bucket_info(bucket_name='testing-buckets-29')
        if bucket_info:
            bucket_info = bucket_info[0]
            bucket.set_working_bucket_id = bucket_info['id']
            bucket.get_files_list()
        # url = "https://testing-buckets-29.s3.us-east-2.amazonaws.com/hello.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZNI2MI2SQKXK6KKZ%2F20221231%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20221231T091644Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=def54f00949cc797bcdb6527a9901bea930b871b26ef25639134bd78fbafa162"
        # url = "/media/1/storagebuckets/1/testing/1672135811_ca60b0e9-5eaf-41da-aff2-1349e603019e.png"
        # bucket.get_file(
        #     filename='bhuwan.png',
        #     bucket_type='Local',
        #     url=url
        #     )
        bucket.post_file("unknown-testing2.png", "C:/Users/user/Desktop/bots/QuickFox/quickrpa-backend-code/bot-starter-kit-v2.0/image_2022_12_31T07_01_32_323Z.png")

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


