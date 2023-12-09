from PySide6.QtCore import QObject, QThread, Signal
from enum import Enum
from core.board import Board


class GameMode(Enum):
    SELF_PLAY = 1
    PLAY_WITH_BOT = 2
    PLAY_ONLINE = 3


class GameplayThread(QThread):
    move_piece_signal = Signal(int, int)

    def init_game(self, game_mode: GameMode, player_names, start_player=0):
        self.game_mode = game_mode
        self.player_names = player_names
        self.start_player = start_player
        self.cur_player = 0
        self.board = Board()
        self.board.init_board(self.start_player)

    def run(self):
        while self.board.game_finished():
            self.move_piece_signal.emit(0, 0)
            self.msleep(1000)  # Simulate some work
