from robot.libraries.BuiltIn import BuiltIn
from RPA.Browser.Selenium import Selenium
from qrlib.QRRunItem import QRRunItem
from qrlib.QRComponent import QRComponent

browser: Selenium = BuiltIn().get_library_instance("RPA.Browser.Selenium")

class ShareSansarComponent(QRComponent):
    
    def __init__(self):
        self.run_item: QRRunItem = None

    def setup(self):
        pass

    def teardown(self):
        pass

    def get_headlines(self):
        try:
            browser.wait_until_element_is_visible("//ul[@class='news-list gl-list']//a", timeout=60)
            headlines = browser.find_elements("//ul[@class='news-list gl-list']//a")
            self.run_item.logger.info("Found news elements")
            return headlines
        except Exception as e:
            self.run_item.logger.error("Failed to get news")
            self.run_item.notification.data = {"reason": "Failed to get news"}
            raise e





