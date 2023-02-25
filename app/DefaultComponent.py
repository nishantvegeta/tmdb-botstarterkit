from qrlib.QRComponent import QRComponent


class DefaultComponent(QRComponent):
    
    def __init__(self):
        super().__init__()

    def login(self):
        try:
            self.run_item.logger.info("Logging in...")
        except Exception as e:
            self.run_item.logger.error("Failed to login")
            self.run_item.notification.data = {"reason": "Login failed"}
            raise e
            
    def logout(self):
        try:
            self.run_item.logger.info("Logging out...")
        except Exception as e:
            self.run_item.logger.error("Failed to logout")
            raise e

    def test(self):
        try:
            self.run_item.logger.info("Test task")
        except Exception as e:
            self.run_item.logger.error("Test task failed")
            raise e
