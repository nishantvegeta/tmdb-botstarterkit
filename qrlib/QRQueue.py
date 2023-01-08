import urllib
from qrlib.QRQueueItem import QRQueueItem
from typing import List
from qrlib.QREnv import QREnv
from robot.libraries.BuiltIn import BuiltIn
import requests

from qrlib.QRQueueItem import QueueItemStatus
from qrlib.QRUtils import display
from qrlib.queue.queue_exceptions import BaseUrlNotSetException, IdentifierNotSetException

class QRQueue:

    def __init__(self, name: str,id=None) -> None:
        self.name = name
        self.id = id
        self.queue_items = []
        
    def get_info(self):
        if(QREnv.NO_PLATFORM):
            return True
        else:
            pass

    def gen_uri(self,params:dict=None):
        if hasattr(QREnv,'BASE_URL'):
            base_url = QREnv.BASE_URL
        else:
            raise BaseUrlNotSetException()

        path = f"bot/queue/"
        uri = urllib.parse.urljoin(base_url, path)
        
        """Not Implemented"""
        if params:
            pass

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
    
    def get_items(self, count: int = 1, order: str = "asc",seek_local=False) -> List[QRQueueItem]:
        if(QREnv.NO_PLATFORM):
            #Read from sample file
            return [QRQueueItem(id=0,status="New",input={"key":"Test"}),QRQueueItem(id=2,status="New",input={"key":"Test1"})]
        else:
            # Hit api to get items. Create queueitems with the response
            response = requests.get(
            url = self.gen_uri(),
            headers=self.gen_headers(),
            params={"name":f"{self.name}", "item_size":count}
            )

        if response.status_code == 200:
            queue_data = response.json()
            #    
            id = queue_data.get("id")
            name = queue_data.get('name')
            queue_items = queue_data.get('queue_items')
            setattr(self,'id',id)
            setattr(self,'name',name)

            for queue_item in queue_items:
                item = QRQueueItem(queue=id,**queue_item)
                self.queue_items.append(item)
            return self.queue_items
        else:
            raise Exception(response.text)
        

    def save(self,mark_all:QueueItemStatus=None,fail_silently=True):
        for item in self.queue_items:
            try:
                if mark_all:
                    item.status = mark_all
                item.save()
            except Exception as e:
                if fail_silently:
                    pass
                else:
                    raise e


    def validate(self):
        """ Not Implemented """
        pass

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
