from abc import ABC, abstractmethod

class QRComponent(ABC):

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def teardown(self):
        pass
