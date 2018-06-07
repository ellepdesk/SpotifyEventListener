from time import sleep

import logging
from pydbus import SessionBus
from collections import Callable


logger = logging.getLogger()


class NotifyDBus():
    def __init__(self, bus):
        self.bus = bus
        self._notifications = None

    def register_event(self, callback):
        if not isinstance(callback, Callable):
            raise ValueError("Callback must be callable, got: {}".format(callback))
        logger.debug("registering notification events")
        return self.notifications.ActionInvoked.connect(lambda *event: callback(["dbus", "Notification", event]))

    def register_closed(self, callback):
        if not isinstance(callback, Callable):
            raise ValueError("Callback must be callable, got: {}".format(callback))
        logger.debug("registering notification close")
        return self.notifications.NotificationClosed.connect(lambda *event: callback(["dbus", "Notification", event]))

    def plug(self):
        logger.debug("plug")
        notification_id = self.notifications.Notify('Headphones', 0, 'audio-headphones', "Headphones plugged in", "resuming spotify",
                                               ["cancel_play", "cancel"], {}, 5000)
        return notification_id

    def unplug(self):
        notification_id = self.notifications.Notify('Headphones', 0, 'audio-headphones', "Headphones removed", "pausing spotify",
                                               ["cancel_pause", "cancel"], {}, 5000)
        return notification_id

    @property
    def notifications(self):
        if not self._notifications:
            self._notifications = self.bus.get('.Notifications')
        return self._notifications


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    from gi.repository import GLib
    nb = NotifyDBus(SessionBus())
    nb.register_event(print)
    nb.register_closed(print)

    nb.plug()
    GLib.MainLoop().run()