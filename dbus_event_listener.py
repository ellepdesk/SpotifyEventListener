import logging
from pydbus import SessionBus

from collections import Callable


def register_screensaver(bus, callback):
    if not isinstance(callback, Callable):
        raise ValueError("Callback must be callable, got: {}".format(callback))
    screensaver = bus.get("org.gnome.ScreenSaver")
    return screensaver.ActiveChanged.connect(lambda event: callback(["dbus", "org.gnome.ScreenSaver.Active", event]))

if __name__ == '__main__':
    register_screensaver(print)
