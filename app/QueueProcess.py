from qrlib.QRProcess import QRProcess
from qrlib.QRRunItem import QRRunItem
from robot.libraries.BuiltIn import BuiltIn
from qrlib.QREnv import QREnv


class QueueProcess(QRProcess):
    
    def __init__(self):
        self.queue = None
        self.vault = None
        self.storage = None

    def set_data(self,queue,vault,storage):
        self.queue = queue
        self.vault = vault
        self.storage = storage


    def run_item(self, queue, queue_item):
        try:
            queue_item.output_from_runitem = True
            run_item = QRRunItem(queue=queue, queue_item=queue_item)
            run_item.report_data = {"a":"b"}  
            #Do operation
            run_item.success()
        except Exception as e:
            run_item.error()
            run_item.post()
            raise e
        run_item.post()

    
    def run(self):
        while(1):
            try:
                run_item = QRRunItem(is_ticket=False)
                queue_items = self.queue.get_items()
                run_item.logger.info('Queue fetched successfully')
                #All good, no need to post run item
            except Exception as e:
                run_item.logger.error('Queue fetch error')
                run_item.error()
                run_item.post()
                raise e
        
            if(queue_items):
                for queue_item in queue_items:
                    BuiltIn().run_keyword("QueueProcess.Process Item", self.queue, queue_item)
            else:
                break

            if(QREnv.NO_PLATFORM):
                break
