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
        # BuiltIn().run_keyword("DefaultProcess.Run")

        # num_threads = len(variables.TELNET_PORT)

        # q = Queue(maxsize=0)

        # for data in overall_data[:10]:
        #     q.put_nowait(data)

        # gevent.joinall([gevent.spawn(work_on_ofs, q, i) for i in range(num_threads)])


    # def work_on_ofs(data,q,thread_no):
    #     try:
    #         dp = DefaultProcess(port=variables.TELNET_PORT[thread_no])
    #         dp.before_run()
    #     except Exception as e:
    #         raise e

    #     while not q.empty():
    #         data = q.get()
    #         dp.execute_run_item(data)

        
    def teardown(self):
        return
        self.dp.after_run()
