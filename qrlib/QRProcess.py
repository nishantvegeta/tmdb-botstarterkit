from abc import ABC, abstractmethod

class QRProcess(ABC):
    
    @abstractmethod
    def update_component_run_item(self):
        pass

    @abstractmethod
    def pre_run_item(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute_run_item(self, *args, **kwargs):
        pass

    @abstractmethod
    def post_run_item(self, *args, **kwargs):
        pass

    @abstractmethod
    def pre_run(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def post_run(self, *args, **kwargs):
        pass