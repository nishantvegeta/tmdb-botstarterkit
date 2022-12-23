from robot.libraries.BuiltIn import BuiltIn
from RPA.Browser.Selenium import Selenium
from qrlib.QRComponent import QRComponent
from qrlib.QRRunItem import QRRunItem
from qrlib.QREnv import QREnv

from qrlib.QRQueue import QRQueue
from qrlib.QRQueueItem import QueueItemStatus
from qrlib.QRUtils import display

class DefaultComponent(QRComponent):
    
    def __init__(self, process):
        super().__init__(process)


    def login(self):
        try:
            self.run_item.logger.info("Logging in...")
        except Exception as e:
            self.run_item.logger.error("Failed to login")
            self.run_item.notification.data = {"reason": "Login failed"}
            raise e

    def logout(self):
        try:
            self.run_item.logger.info("Logging out...")
        except Exception as e:
            self.run_item.logger.error("Failed to logout")
            raise e

    def test(self):
        try:
            self.run_item.logger.info("Test task")
        except Exception as e:
            self.run_item.logger.error("Test task failed")
            raise e


    def get_queue_items(self):
        queue_test = QRQueue(name="test")
        queue_items = queue_test.get_items()
        return queue_items

    def change_queue_items(self,queue_items):
        for item in queue_items:
            # display(item.id)
            # display(item.input)
            # display(item.status.value)

            item.status=QueueItemStatus.ERROR
            item.input = {"b":"b"}
            item.output = {"c":"c"}
            save_status = item.save()
            display(save_status)
