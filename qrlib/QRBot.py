from abc import ABC, abstractmethod

class QRBot(ABC):

    @abstractmethod
    def update_component_run_item(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def teardown(self):
        pass
