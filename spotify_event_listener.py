import logging
from gi.repository import GLib
from spotify_dbus import SpotifyDBus
from acpi_event_listener import AcpiEventListener
from dbus_event_listener import register_screensaver
from notify_dbus import NotifyDBus
from pydbus import SessionBus

logger = logging.getLogger(__name__)


class SpotifyEventListener():
    def __init__(self):
        bus = SessionBus()
        register_screensaver(bus, callback=self.translate_events)
        self.acpi_listener = AcpiEventListener(callback=self.translate_events)
        self.spotify = SpotifyDBus(bus)
        self.was_playing = False
        self.notify = NotifyDBus(bus)
        self.notify.register_event(self.translate_events)

    def translate_events(self, event):
        logger.info(event)
        if event[0] == 'acpi' and event[1] == 'jack/headphone' and event[2] == 'HEADPHONE':
            if event[3] == 'plug':
                logger.info("Headphones plugged in")
                self.spotify.command("Play")
                self.notify.plug()
            if event[3] == 'unplug':
                logger.info("Headphones removed")
                self.was_playing = self.spotify.is_playing()
                self.notify.unplug()
                logger.info("pausing spotify")
                self.spotify.command("Pause")

    @classmethod
    def run(cls):
        try:
            self = cls()
            self.acpi_listener.start()
            print("MAINLOOP")
            GLib.MainLoop().run()


        except:
            GLib.MainLoop().quit()
            self.acpi_listener.stop()
            print("MAINLOOP END")


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', level=logging.INFO)
    SpotifyEventListener.run()
