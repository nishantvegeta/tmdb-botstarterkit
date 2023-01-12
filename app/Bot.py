from qrlib.QRBot import QRBot
from robot.libraries.BuiltIn import BuiltIn
from DefaultProcess import DefaultProcess
from qrlib.QREnv import QREnv

class Bot(QRBot):

    def __init__(self):
        super().__init__()
        self.dp = BuiltIn().get_library_instance("DefaultProcess")

    def start(self):
        self.setup_platform_components()
        self.dp.before_run()
        self.dp.run()

    def teardown(self):
        return
        self.dp.after_run()
