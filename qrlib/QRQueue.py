from qrlib.QRQueueItem import QRQueueItem
from typing import List
from qrlib.QREnv import QREnv
import requests
from qrlib.queue.queue_exceptions import BaseUrlNotSetException, IdentifierNotSetException

class QRQueue:

    def __init__(self, name: str) -> None:
        self.name = name
        self.id = None
        
    def get_info(self):
        if(QREnv.NO_PLATFORM):
            return True
        else:
            pass

    @staticmethod        
    def gen_uri(params:dict=None):
        if hasattr(QREnv,'BASE_URL'):
            base_url = QREnv.BASE_URL
        else:
            raise BaseUrlNotSetException()

        path = f"/bot/queue/"
        uri = f"{base_url}{path}"
        
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
            return [QRQueueItem(id=0,status="New",queue=0,input={"key":"Test"}),QRQueueItem(id=2,status="New",queue=0,input={"key":"Test1"})]
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
                queue_items_list = []
                for queue_item in queue_items:
                    item = QRQueueItem(queue=id,**queue_item)
                    queue_items_list.append(item)
                return queue_items_list
            else:
                raise Exception(response.text)
                
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
