from qrlib.QRLogger import QRLogger
from qrlib.QRQueue import QRQueue
from qrlib.QRQueueItem import QRQueueItem
from qrlib.QRRunItemNotification import QRRunItemNotification
from qrlib.QREnv import QREnv
import requests
from robot.libraries.BuiltIn import BuiltIn
import traceback
import logging


class QRRunItem:

    def __init__(self, logger_name: str = 'quickrpa_default_logger', is_ticket=True, queue: QRQueue = None, queue_item: QRQueueItem = None) -> None:
        self.started_at = BuiltIn().get_time()
        self.completed_at = None
        self.status = None
        self.bot_logger = QRLogger(logger_name)
        self.logger = self.bot_logger.logger
        self.queue = queue
        self.queue_item = queue_item
        self.is_ticket = is_ticket
        self.report_data = {}
        self.notification = QRRunItemNotification()

    def set_bot_logger(self, bot_logger):
        self.bot_logger = bot_logger
        self.logger = self.bot_logger.logger

    def set_report_data_item(self, key, value) -> None:
        self.report_data[key] = value

    def error(self, trace=True) -> None:
        self.status = 'Error'
        if (self.is_ticket and self.queue_item):
            self.queue_item.error()
        if (trace):
            self.log_trace()

    def success(self) -> None:
        self.status = 'Completed'
        if (self.is_ticket and self.queue_item):
            self.queue_item.success()

    def post(self) -> None:
        self.completed_at = BuiltIn().get_time()
        log_text = self.bot_logger.get_log_contents()
        self.bot_logger.clear_logs()
        self.bot_logger.close_logger()
            
        # Using temp logger in case of any issue posting runitem since we've closed bot logger.
        
        temp_logger = logging.getLogger(__name__)

        # post queue item
        try:
            if (self.is_ticket and self.queue and self.queue_item):
                if (self.queue_item.output_from_runitem):
                    self.queue_item.output = self.report_data
                if (not self.queue_item.output):
                    raise Exception('Queue item has no output')
                
                self.queue.post(self.queue_item)
        except Exception as e:
            temp_logger.error("Error posting queue item")
            temp_logger.error(traceback.format_exc())
            raise e

        try:
            if(QREnv.NO_PLATFORM):
                temp_notification = self.notification.get_notification_dict()
                if('attachments' in temp_notification):
                    temp_notification.pop('attachments')
                run_item_dict = {
                    "started_at": self.started_at,
                    "completed_at": self.completed_at,
                    "status": self.status,
                    "report_data": self.report_data,
                    "is_ticket": self.is_ticket,
                    "notification": temp_notification,
                }
                BuiltIn().log(f"Run Item: {run_item_dict}", console=True)
            else:
                # Get runitem info
                run_item_dict = {
                    "started_at": self.started_at,
                    "completed_at": self.completed_at,
                    "status": self.status,
                    "report_data": self.report_data,
                    "log_text": log_text,
                    "is_ticket": self.is_ticket,
                    "notification": self.notification.get_notification_dict()
                }

                runitem_url = f"{QREnv.BASE_URL}/runitems-request/{QREnv.IDENTIFIER}/"
                # Post runitem
                response = requests.post(
                    url=runitem_url,
                    json=run_item_dict,
                    verify=QREnv.VERIFY_SSL
                )
                if response.status_code == 200:
                    return True
                else:
                    temp_logger.error(response.text)
                    raise Exception(
                        f'Received status code of {response.status_code}')
        except Exception as e:
            temp_logger.error("Error posting run item")
            temp_logger.error(traceback.format_exc())
            raise e
            

    def log_trace(self) -> None:
        trace = traceback.format_exc()
        self.logger.error(trace)
