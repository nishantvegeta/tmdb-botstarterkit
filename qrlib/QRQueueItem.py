class QRQueueItem:

    def __init__(self, id: int, status: str, input: dict, output_from_runitem: bool = True) -> None:
        if not id:
            raise Exception('Queue Item status must be new for a new queue item')

        self.id = id
        self.status = status
        self.input = input
        self.output = {}
        self.output_from_runitem = output_from_runitem

    def error(self) -> None:
        self.status = 'Error'

    def success(self) -> None:
        self.status = 'Completed'
