import socket
import logging
from collections import Callable
from threading import Thread, Event

logger = logging.getLogger(__name__)


class AcpiEventListener(Thread):
    def __init__(self, callback=None, path='/var/run/acpid.socket'):
        super().__init__(name=__name__, daemon=True)
        logger.info('connecting to {}'.format(path))
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(path)
        self.handle = self.sock.makefile()
        self.callback = callback
        self.running = Event()
        if not isinstance(callback, Callable):
            raise ValueError("Callback must be callable, got: {}".format(callback))

    def run(self):
        self.running.set()
        try:
            while self.running.is_set():
                data = self.handle.readline().rstrip()
                if not data:
                    raise EOFError
                logger.debug('received "{}"'.format(data))
                event = ["acpi"] + data.split(" ")
                self.callback(event)
        finally:
            self.handle.close()
            self.sock.close()

    def stop(self):
        self.running.clear()
        self.sock.close()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', level=logging.DEBUG)
    sut = AcpiEventListener(callback=logging.info)
    sut.run()
