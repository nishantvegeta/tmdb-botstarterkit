from abc import ABC, abstractmethod
from qrlib.QRObserver import QRPublisher
from qrlib.QRRunItem import QRRunItem

class QRProcess(ABC, QRPublisher):

    def __init__(self):
        for base_class in QRProcess.__bases__:
             base_class.__init__(self)
        self.run_item: QRRunItem = None

    @abstractmethod
    def before_run_item(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute_run_item(self, *args, **kwargs):
        pass

    @abstractmethod
    def after_run_item(self, *args, **kwargs):
        pass

    @abstractmethod
    def before_run(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def after_run(self, *args, **kwargs):
        pass