from PySide6.QtCore import QThread, Signal, QPoint
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
        self.piece_selected = False  # player has to select the piece first to move it
        self.selected_piece = 0
        self.cur_player_finished = False
        self.board = Board()
        self.board.init_board(self.start_player)

    def run(self):
        while True:
            if not self.board.game_finished():
                self.cur_player_finished = False
                while not self.cur_player_finished:
                    self.msleep(10)
                    # self.move_piece_signal.emit(0, 0)
                    # self.msleep(1000)  # Simulate some work
            else:
                pass

    def handle_user_input(self, coord: QPoint):
        x, y = coord.x(), coord.y()
        piece_idx = self.board.cur_state[x, y]
        print(f"GameplayThread: user {self.player_names[self.cur_player]} input coord {coord}, piece_idx: {piece_idx}")
        self.cur_player = 1 - self.cur_player  # switch the player
        self.cur_player_finished = True

        # # select the piece
        # if piece_idx != 0 and (piece_idx > 0) == (self.cur_player == 0):  # check it's a valid piece
        #     self.piece_selected = piece_idx
        #     self.piece_selected = True

        # else:
        #     # move the piece to the new coord
        #     if piece_idx == 0:  # check it's a new coord
        #         self.piece_selected = False
        #         self.cur_player = 1 - self.cur_player  # switch the player
        #         self.cur_player_finished = True

