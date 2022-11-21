from QRObserver import QRSubscriber
from qrlib.QRObserver import QRPublisher
from qrlib.QRRunItem import QRRunItem

class QRComponent(QRSubscriber):

    def __init__(self):
        self.run_item: QRRunItem = None

    def update(self, publisher: QRPublisher):
        self.run_item = publisher.run_item