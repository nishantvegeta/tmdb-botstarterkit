from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item_tt, run_item_tf
from qrlib.QRStorageBucket import QRStorageBucket
from DefaultComponent import DefaultComponent
from RPA.Browser.Selenium import Selenium
from robot.libraries.BuiltIn import BuiltIn
from qrlib.QREnv import QREnv


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
        self.run_item.report_data["test"] = args[0]

    @run_item_tf()
    def before_run(self, *args, **kwargs):
        BuiltIn().log_to_console(QREnv.VAULTS)  
        self.default_component.login()
        self.data = ["a", "b"]

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
        self.before_run()
        for x in self.data:
            self.execute_run_item(x)
