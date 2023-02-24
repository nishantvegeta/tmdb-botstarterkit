from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from qrlib.QRStorageBucket import QRStorageBucket
from DefaultComponent import DefaultComponent
from RPA.Browser.Selenium import Selenium
from robot.libraries.BuiltIn import BuiltIn
from qrlib.QREnv import QREnv


class DefaultProcess(QRProcess):

    def __init__(self):
        super().__init__()
        self.default_component = DefaultComponent()
        self.register(self.default_component)
        self.data = []


    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        self.default_component.login()
        self.data = ["a", "b"]

    @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        self.default_component.test()
        run_item.report_data["test"] = args[0]


    @run_item(is_ticket=False)
    def after_run(self, *args, **kwargs):
        # Get run item created by decorator. Then notify to all components about new run item.
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        self.default_component.logout()

  
    def execute_run(self):
        for x in self.data:
            self.execute_run_item(x)

