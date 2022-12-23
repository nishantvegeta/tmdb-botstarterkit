import urllib
import requests
from enum import Enum
import pydantic
from qrlib.QREnv import QREnv
from qrlib.queue.queue_exceptions import BaseUrlNotSetException, IdentifierNotSetException, PatchRequestFailedException

class QueueItemStatus(Enum):
        COMPLETED = "Completed"
        ERROR = "Error"
        NEW = "New"
        PROCESSING = "Processing"
        ARCHIVED = "Archived"


        @property
        def transitions(cls):
            TRANSITIONS = {
                cls.NEW: [cls.NEW, cls.ARCHIVED, cls.PROCESSING],
                cls.PROCESSING: [cls.PROCESSING,cls.PROCESSING,cls.ARCHIVED,cls.NEW,cls.ERROR,cls.COMPLETED],
                cls.COMPLETED: [cls.COMPLETED],
                cls.ERROR: [cls.NEW],
                cls.ARCHIVED: [cls.ARCHIVED],
            }
            return TRANSITIONS

        @property
        def choices(cls):
            return [i.value for i in cls]

         
class QRQueueItem(pydantic.BaseModel):
    id : int
    status:QueueItemStatus
    input: dict
    output: dict = {}
    queue:int

    class Config:  
        use_enum_values = True

    def set_error(self) -> None:
        self.status = QueueItemStatus.ERROR

    def set_success(self) -> None:
        self.status =  QueueItemStatus.COMPLETED

    def set_retry(self)->None:
        self.status =  QueueItemStatus.NEW

    def gen_uri(self):
        if hasattr(QREnv,'BASE_URL'):
            base_url = QREnv.BASE_URL
        else:
            raise BaseUrlNotSetException()

        path = f"bot/queue/{self.queue}/data/{self.id}/"
        uri = urllib.parse.urljoin(base_url, path)
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

    def save(self):
        json_data = self.dict()
        
        response = requests.patch(
        url = self.gen_uri(),
        json=json_data,
        headers=self.gen_headers()
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise PatchRequestFailedException(response.text)
