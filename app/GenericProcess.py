from qrlib.QRProcess import QRProcess
from qrlib.QRRunItem import QRRunItem
from robot.libraries.BuiltIn import BuiltIn
from qrlib.QREnv import QREnv
from qrlib.QRDecorators import run_item_tt, run_item_tf
from ShareSansarComponent import ShareSansarComponent
from RPA.Browser.Selenium import Selenium

browser: Selenium = BuiltIn().get_library_instance("RPA.Browser.Selenium")

class GenericProcess(QRProcess):
    
    def __init__(self):
        super().__init__()
        self.ss_component = ShareSansarComponent()
        self.run_item: QRRunItem = None

    def update_component_run_item(self):
        self.ss_component.run_item = self.run_item

    @run_item_tt()
    def execute_run_item(self, *args, **kwargs):
        try:
            #Do operation
            if("Sanima" in args[0]):
                raise Exception("Sanima error")
            self.run_item.report_data = {"headline":args[0]} 
        except Exception as e:
            self.run_item.notification.subject = "Error"
            self.run_item.notification.data = {"test":"data"}
            raise e

    @run_item_tf()
    def pre_run(self, *args, **kwargs):  
        self.run_item.logger.info(f"In pre run")
        return self.ss_component.get_headlines()

    @run_item_tf()
    def post_run(self, *args, **kwargs):
        self.run_item.logger.info(f".....In post run")
    
    @run_item_tf()
    def pre_run_item(self, *args, **kwargs):
        self.run_item.logger.info(f"In pre run item = {args[0]}")

    @run_item_tf()
    def post_run_item(self, *args, **kwargs):
        self.run_item.logger.info(f"In post run item = {args[0]}")

    def run(self):
        data = self.pre_run()
        for item in data:
            self.pre_run_item(item.text)
            self.execute_run_item(item.text)
            self.post_run_item(item.text)
            # BuiltIn().run_keyword("GenericProcess.Pre Run Item")
            # BuiltIn().run_keyword("GenericProcess.Run Item",item)
            # BuiltIn().run_keyword("GenericProcess.Post Run Item")
        self.post_run()


