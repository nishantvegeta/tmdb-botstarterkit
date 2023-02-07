from qrlib.QRObserver import QRSubscriber, QRPublisher
from qrlib.QRProcess import QRProcess
from qrlib.QRRunItem import QRRunItem


class QRComponent(QRSubscriber):

    def __init__(self, process: QRProcess):
        self.run_item: QRRunItem = process.run_item
        process.register(self)

    def notify(self, process: QRProcess):
        self.run_item = process.run_item
