# SpotifyEventListener
Daemon to pause/unpause Spotify when headphones are unplugged/plugged

## Use case
I listen music exclusively on headphones, so when I unplug them and my music continues on speakers its always an annoyance.

My laptop knows this, and kindly mutes my speaker when I unplug.

However, Spotify does not know this, and keeps playing my playlist at zero volume.

So in short what I want is: When I unplug my headphones, a notification appears that my headphones are unplugged and Spotify will be paused.
In the odd case that I don't want that, a cancel button should cancel the pause before it is executed.

When I plus my headphones back in, I want to be able to quickly resume Spotify, either automatically-but-cancellable or when I press a button (I haven't decided yet).

Finally, the same logic applies when I lock my laptop, after a short grace period Spotify should stop playing and resume as soon as I unlock


## Installation
TODO

## Requirements
Python 3.4+ or 2.7+(probably)
pydbus
...more


## Implementation
The daemon is written in python, as I'm currently the most active in that language.

The headphone plug/unplug events are coming from acpi, I wrote a small tool to read the unix-socket at '/var/run/acpid.socket'
Notifications, controlling Spotify and listening to lock/unlock events are all possible using DBus,
using the [pydbus](https://github.com/LEW21/pydbus) python interface


