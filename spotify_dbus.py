import logging
from collections import Callable

logger = logging.getLogger(__name__)


class SpotifyDBus():
    def __init__(self, bus):
        self._spotify = None
        self.bus = bus

    def command(self, cmd):
        try:
            logger.info("Executing command {}".format(cmd))
            attribute = getattr(self.spotify, cmd)
            if isinstance(attribute, Callable):
                return attribute()
            else:
                return attribute
        except:
            logger.exception("")
            self._spotify = None

    @property
    def spotify(self):
        if not self._spotify:
            logger.debug("getting endpoint")
            self._spotify = self.bus.get('org.mpris.MediaPlayer2.spotify', "/org/mpris/MediaPlayer2")
        return self._spotify


    def is_playing(self):
        return(self.spotify.PlaybackStatus == "Playing")


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', level=logging.DEBUG)
    spotify = SpotifyDBus()
    print(spotify.is_playing())
    print(spotify.command("Play"))
