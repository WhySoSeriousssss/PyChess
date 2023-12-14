from enum import Enum


class GameMode(Enum):
    SELF_PLAY = 1
    PLAY_WITH_BOT = 2
    BOT_COMBAT = 3
    PLAY_ONLINE = 4