import logging
from threading import Thread
from gi.repository import GLib

logger = logging.getLogger(__name__)


class GLibMainLoop(Thread):
    mainloop = GLib.MainLoop()

    def __init__(self):
        super().__init__(name=__name__, daemon=True)

    def run(self):
        logger.debug("starting GLib mainloop")
        self.mainloop.run()
        logger.debug("stopped GLib mainloop")

    def stop(self):
        logger.debug("stopping GLib mainloop")
        self.mainloop.quit()
