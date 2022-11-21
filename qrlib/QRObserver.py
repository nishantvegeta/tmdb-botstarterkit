from abc import ABC, abstractmethod

class QRSubscriber(ABC):

    @abstractmethod
    def update(self, publisher) -> None:
        pass
        

class QRPublisher:

    def __init__(self):
        self._subscribers = set()

    def register(self, subscriber: QRSubscriber) -> None:
        self._subscribers.add(subscriber)

    def unregister(self, subscriber: QRSubscriber) -> None:
        self._subscribers.discard(subscriber)

    def notify(self) -> None:
        for subscriber in self._subscribers:
            subscriber.update(self)