from qrlib.QRBot import QRBot
from qrlib.QRQueue import QRQueue
from qrlib.QRStorageBucket import QRStorageBucket
from qrlib.QRRunItem import QRRunItem
import qrlib.QRUtils
from robot.libraries.BuiltIn import BuiltIn
from qrlib.QREnv import QREnv
from qrlib.QRDecorators import run_item_tf
from RPA.Browser.Selenium import Selenium

browser: Selenium = BuiltIn().get_library_instance("RPA.Browser.Selenium")

class Bot(QRBot):
    
    def __init__(self):
        self.queues: dict[str, QRQueue] = {}
        self.storages: dict[str, QRStorageBucket] = {}
        self.vaults = {}
        self.run_item: QRRunItem = None

    def update_component_run_item(self):
        pass

    def setup_bot_components(self): 
        try:      
            self.run_item.logger.info("Opening browser...")
            browser.open_available_browser("https://www.sharesansar.com/")
            self.run_item.logger.info("Opened browser...")
            self.run_item.report_data = {"this":"success"}
        except Exception as e:
            self.run_item.logger.error("Couldn't open browser")
            raise e


    def start(self):
        if(QREnv.TEST_SETUP_ONLY):
            return

        gp = BuiltIn().get_library_instance("GenericProcess")
        BuiltIn().run_keyword("GenericProcess.Run")


    def teardown(self):
        browser.close_all_browsers()


    @run_item_tf(post_success=True)
    def setup(self, *args, **kwargs):
        BuiltIn().run_keyword("Setup Platform Components")
        BuiltIn().run_keyword("Setup Bot Components")


    def setup_platform_components(self):
        for vault_name in QREnv.VAULTS:
            try:
                self.vaults[vault_name] = qrlib.QRUtils.get_secret(vault_name)
                self.run_item.logger.info(f"Retrieved vault: {vault_name}")
            except Exception as e:
                self.run_item.logger.error(f"Failed to retrieve vault: {vault_name}")
                self.run_item.notification.set(subject=f"Warning! {QREnv.BOT_NAME} bot has stopped unexpectedly", data={"reason":f"Failed to retrieve vault: {vault_name}"})
                raise e

        for queue_name in QREnv.QUEUES:
            try:
                queue = QRQueue(queue_name)
                queue.get_info()
                self.queues[queue_name] = queue
                self.run_item.logger.info(f"Retrieved queue info: {queue_name}")
            except Exception as e:
                self.run_item.logger.error(f"Failed to retrieve queue info: {queue_name}")
                self.run_item.notification.set(subject=f"Warning! {QREnv.BOT_NAME} bot has stopped unexpectedly", data={"reason":f"Failed to retrieve queue info: {queue_name}"})
                raise e

        for storage_name in QREnv.STORAGES:
            try:
                storage = QRStorageBucket(storage_name)
                storage.get_info()
                self.storages[storage_name] = storage
                self.run_item.logger.info(f"Retrieved storage info: {storage_name}")
            except Exception as e:
                self.run_item.logger.error(f"Failed to retrieve storage info: {storage_name}")
                self.run_item.notification.set(subject=f"Warning! {QREnv.BOT_NAME} bot has stopped unexpectedly", data={"reason":f"Failed to retrieve storage info: {storage_name}"})
                raise e

    
        
