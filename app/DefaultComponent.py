from qrlib.QRComponent import QRComponent

from RPA.Browser.Selenium import Selenium

from Utils import read_vaultfile

class DefaultComponent(QRComponent):
    
    def __init__(self):
        super().__init__()
        self.sel = Selenium(auto_close=False)

    def login(self):
        data = read_vaultfile()

        username = data['username']
        password = data['password']
        self.logger.info(username)
        self.logger.info(password)
        try:
            self.logger.info("Logging in...")
        except Exception as e:
            self.run_item.logger.error("Failed to login")
            self.run_item.notification.data = {"reason": "Login failed"}
            raise e
            
    def logout(self):
        try:
            self.logger.info("Logging out...")
        except Exception as e:
            self.logger.error("Failed to logout")
            raise e

    def test(self):
        try:
            self.logger.info("Test task")
        except Exception as e:
            self.logger.error("Test task failed")
            raise e
