from qrlib.QRQueueItem import QRQueueItem
from typing import List
from qrlib.QREnv import QREnv
from robot.libraries.BuiltIn import BuiltIn


class QRQueue:

    def __init__(self, name: str) -> None:
        self.name = name

    def get_info(self):
        if(QREnv.NO_PLATFORM):
            return True
        else:
            pass

    def get_items(self, count: int = 1, order: str = "asc") -> List[QRQueueItem]:
        if(QREnv.NO_PLATFORM):
            #Read from sample file
            return [QRQueueItem(id=1,status="New",input={"key":"Test"}),QRQueueItem(id=2,status="New",input={"key":"Test1"})]
        else:
            # Hit api to get items. Create queueitems with the response
            responses = []
            queue_items = []
            for response in responses:
                item = QRQueueItem(response.id, response.status, response.input)
                queue_items.append(item)
            return queue_items

    def post(self, item: QRQueueItem) -> None:
        if not (item.status == 'Error' or item.status == 'Completed' or item.status == 'Retry'):
            raise Exception(f"Invalid queue item status while posting. Should be Error, Completed or Retry. Found {item.status}")
        if(not item.output):
            raise Exception(f"Queue item must have valid output")
        
        if(QREnv.NO_PLATFORM):
            item_dict = {'queue':self.name,'id':item.id,'input':item.input,'output':item.output,'output_from_runitem':item.output_from_runitem}
            BuiltIn().log(f"Queue Item: {item_dict}", console=True)
        else:
            pass

    def create_new_items_from_list(self, items: list) -> None:
        if(QREnv.NO_PLATFORM):
            return True
        else:
            pass

    def create_new_items_from_csv(self, file_path: str) -> None:
        if(QREnv.NO_PLATFORM):
            return True
        else:
            pass
