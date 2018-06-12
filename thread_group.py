import threading
from queue import Queue, Empty
import logging
import signal
import time
import sys
import types

logger = logging.getLogger(__name__)


class ThreadGroup():
    def __init__(self, timeout=1, enable_signal_handler=False):
        self.threads = []
        self.exception_queue = Queue()
        self.timeout = timeout
        self.running = threading.Event()
        if enable_signal_handler:
            logger.info("adding signal handlers")
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, sig, frame):
        """Handle signal, restore system handle and stop all components"""
        logging.error('Caught signal: {}, stopping'.format(sig))
        # restore signal handler
        signal.signal(sig, signal.SIG_DFL)
        self.exception_queue.put(KeyboardInterrupt("Interrupted"))
        #self.stop()

    @staticmethod
    def _inject_error_handler(thread, exception_queue):
        thread.real_run = thread.run
        thread.exception_queue = exception_queue

        def safe_run(self):
            try:
                self.real_run()
            except Exception as e:
                logger.debug("pushing exception to queue {}".format(type(e)))
                logger.exception(e)
                self.exception_queue.put(e)

        # bind instance of safe_run to thread.run
        thread.run = types.MethodType(safe_run, thread)

    def add(self, thread):
        if not isinstance(thread, threading.Thread):
            raise ValueError("ThreadGroup can only be used for Threads")
        logger.debug("adding thread: {}".format(thread.name))
        self._inject_error_handler(thread, self.exception_queue)
        self.threads.append(thread)

    def run(self):
        logger.info("starting threads")
        for th in self.threads:
            logger.debug("starting thread: {}".format(th.name))
            th.start()
        logger.info("started all threads")
        self.running.set()
        while self.running.is_set():
            if not any([th.isAlive() for th in self.threads]):
                self.running.clear()
            try:
                err = self.exception_queue.get(timeout=self.timeout)
            except Empty:
                continue
            raise err

    def stop(self):
        logger.info("stopping threads")
        for th in self.threads:
            logger.info("stopping thread: {}".format(th.name))
            try:
                th.stop()
            except:
                logger.exception("")
                time.sleep(10)
                sys.exit(-1)
        #self.running.clear()

    def join(self):
        logger.info("joining all threads")
        for th in self.threads:
            if th.isAlive():
                logger.debug("joining thread: {}".format(th.name))
                th.join()
