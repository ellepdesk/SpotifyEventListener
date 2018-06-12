import logging
from spotify_dbus import SpotifyDBus
from acpi_event_listener import AcpiEventListener
from dbus_event_listener import register_screensaver
from notify_dbus import NotifyDBus
from pydbus import SessionBus
from thread_group import ThreadGroup
from glib_mainloop import GLibMainLoop
from event_scheduler import EventScheduler

logger = logging.getLogger(__name__)


class SpotifyEventListener(ThreadGroup):
    def __init__(self):
        super().__init__(enable_signal_handler=True)
        bus = SessionBus()
        register_screensaver(bus, callback=self.event_handler)
        self.add(AcpiEventListener(callback=self.event_handler))
        self.add(GLibMainLoop())
        self.spotify = SpotifyDBus(bus)
        self.notify = NotifyDBus(bus, callback=self.event_handler)
        self.scheduler = EventScheduler()
        self.add(self.scheduler)

    def play(self):
        self.scheduler.cancel('Pause')
        self.spotify.command('Play')

    def pause(self):
        self.scheduler.cancel('Play')
        self.spotify.command('Pause')

    def event_handler(self, event):
        if event == ['acpi', 'jack/headphone', 'HEADPHONE', 'plug']:
            logger.info("Headphones plugged in")
            self.notify.plug()
            self.play()

        elif event == ['acpi', 'jack/headphone', 'HEADPHONE', 'unplug']:
            logger.info("Headphones removed")
            self.spotify.is_playing()
            self.notify.unplug()
            self.scheduler.add(identifier='pause', delay=5, action=self.pause)

        elif event == ['dbus', 'ScreenSaver', True]:
            self.scheduler.add(identifier='Pause', delay=5, action=self.pause)

        elif event == ['dbus', 'ScreenSaver', False]:
            self.notify.unlock()
            self.scheduler.add(identifier='Play', delay=5, action=self.play)

        elif event[:2] == ['dbus', 'Notification']:
            if event[2][1] == 'cancel_pause':
                self.scheduler.cancel("Pause")
            if event[2][1] == 'cancel_play':
                self.scheduler.cancel("Play")
        else:
            logger.info(event)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', level=logging.DEBUG)
    instance = SpotifyEventListener()
    try:
        instance.run()
    except:
        logger.exception("")
    finally:
        instance.stop()
