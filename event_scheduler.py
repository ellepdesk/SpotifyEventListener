from time import sleep
import logging
from sched import scheduler
from threading import Thread, Event

logger = logging.getLogger(__name__)


class EventScheduler(Thread):
    def __init__(self):
        super().__init__(name=__name__, daemon=True)
        self.sched = scheduler()
        self.events = {}

    def add(self, identifier, delay, action, argument=(), kwargs={}):
        ref = self.sched.enter(delay=delay, priority=5, action=action, argument=argument , kwargs=kwargs)
        logger.info(ref)
        self.events[identifier] = ref

    def run(self):
        while True:
            self.sched.run(blocking=True)
            self.events = {}
            sleep(1)

    def cancel(self, identifier):
        event = self.events.get(identifier)
        try:
            self.sched.cancel(event)
        except ValueError:
            pass

    def stop(self):
        for event in self.sched.queue:
            try:
                self.sched.cancel(event)
            except ValueError:
                pass
