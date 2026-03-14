from core.settings import (
    pygame,
    join,
    BUTTON_SOUNDS_FILEPATH,
    PIECE_SOUNDS_FILEPATH,
    SLIDER_SOUNDS_FILEPATH,
)
from core.enums import SoundNames

# initilaize mixer
pygame.mixer.init()

sound_files: dict[str, str] = {
    SoundNames.CAPTURE: join(PIECE_SOUNDS_FILEPATH, "capture.mp3"),
    SoundNames.CASTLE: join(PIECE_SOUNDS_FILEPATH, "castle.mp3"),
    SoundNames.CHECK: join(PIECE_SOUNDS_FILEPATH, "check.mp3"),
    SoundNames.GAME_END: join(PIECE_SOUNDS_FILEPATH, "game-end.mp3"),
    SoundNames.MOVE: join(PIECE_SOUNDS_FILEPATH, "move.mp3"),
    SoundNames.PROMOTE: join(PIECE_SOUNDS_FILEPATH, "promote.mp3"),
    SoundNames.BUTTON_DOWN: join(BUTTON_SOUNDS_FILEPATH, "button-down.mp3"),
    SoundNames.BUTTON_UP: join(BUTTON_SOUNDS_FILEPATH, "button-up.mp3"),
    SoundNames.SLIDER: join(SLIDER_SOUNDS_FILEPATH, "slider.mp3"),
}
"""
relates sound name identifiers to their filepaths
"""

channel_groups: dict[str, list[str]] = {
    "piece": [
        SoundNames.CAPTURE,
        SoundNames.CASTLE,
        SoundNames.CHECK,
        SoundNames.GAME_END,
        SoundNames.MOVE,
        SoundNames.PROMOTE,
    ],
    "button": [SoundNames.BUTTON_DOWN, SoundNames.BUTTON_UP],
    "slider": [SoundNames.SLIDER],
}
"""
relates the channel group name identifier to sound name identifiers.
"""
# reserve channels
pygame.mixer.set_reserved(len(channel_groups))

channels: dict[str, int] = {}
"""
dictionary that maps the sound name to the channel integer
that can be used as such to obtain the channel to play the sound in:

```
channel_for_sound = pygame.mixer.Channel(channels[sound_name])
```
"""
for channel_num, (group, names) in enumerate(channel_groups.items()):
    for name in names:
        channels[name] = channel_num

sounds: dict[str, pygame.Sound] = {}
"""relates a sounds name identifier to its corresponding sound object"""
for sound_name, sound_filepath in sound_files.items():
    sounds[sound_name] = pygame.Sound(sound_filepath)


def get_channel(sound_name: str) -> pygame.Channel:
    return pygame.mixer.Channel(channels[sound_name])


def playsound(sound_name: str) -> None:
    channel = get_channel(sound_name)
    sound = sounds[sound_name]
    channel.play(sound)


def stopsound(sound_name: str) -> None:
    channel = get_channel(sound_name)
    channel.stop()


def is_playing(sound_name: str) -> bool:
    channel = get_channel(sound_name)
    return channel.get_busy() and channel.get_sound() == sounds[sound_name]
