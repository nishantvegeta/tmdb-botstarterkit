from qrlib.QRBot import QRBot
from DefaultProcess import DefaultProcess

class Bot(QRBot):

    def __init__(self):
        super().__init__()
        self.dp = DefaultProcess()

    def start(self):
        self.setup_platform_components()
        self.dp.before_run()
        self.dp.execute_run()

    def teardown(self):
        self.dp.after_run()
