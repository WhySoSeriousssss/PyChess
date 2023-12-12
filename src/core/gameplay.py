from PySide6.QtCore import QThread, Signal
from enum import Enum
from core.board import *


class GameMode(Enum):
    SELF_PLAY = 1
    PLAY_WITH_BOT = 2
    PLAY_ONLINE = 3


class GameplayThread(QThread):
    player_moved_signal = Signal(int, tuple)  # piece_id, coord
    game_finished_signal = Signal(int)  # winner

    def init_game(self, game_mode: GameMode, player_names, start_player=0):
        self.game_mode = game_mode
        self.player_names = player_names
        self.start_player = start_player
        self.cur_player = 0
        self.selected_piece = 0  # the piece the current player selected
        self.cur_player_finished = False  # whether the current player has finished the move
        self.board = Board()
        self.board.init_board(self.start_player)

    def run(self):
        while True:
            game_finished, winner = self.board.game_finished()
            if not game_finished:
                self.cur_player_finished = False
                while not self.cur_player_finished:
                    self.msleep(10)
            else:
                break
        self.game_finished_signal.emit(winner)

    def handle_user_input(self, coord):
        piece_id = self.board.cur_state[coord]

        # first input: piece
        if self.selected_piece == 0:
            # player selected his own piece
            if piece_id != 0 and piece_id_to_owner[piece_id - 1] == self.cur_player:
                self.selected_piece = piece_id
                print(f"GameplayThread: user {self.player_names[self.cur_player]} selected piece_id:{self.selected_piece}. availables:{self.board.availables[self.selected_piece]}")
        # second input: coord
        else:
            # player selected his own piece
            if piece_id != 0 and piece_id_to_owner[piece_id - 1] == self.cur_player:
                # change selected piece
                self.selected_piece = piece_id
                print(f"GameplayThread: user {self.player_names[self.cur_player]} changed to piece_id:{self.selected_piece}. availables:{self.board.availables[self.selected_piece]}")
            # player select a coord, check valid move
            elif self.board.check_move_available(self.selected_piece, coord):
                # make the move
                print(f"GameplayThread: user {self.player_names[self.cur_player]} moved piece_id: {self.selected_piece} to {coord}")
                self.board.move_piece(self.cur_player, self.selected_piece, coord)
                self.player_moved_signal.emit(self.selected_piece, coord)
                self.cur_player = 1 - self.cur_player  # switch the player
                # reset variables
                self.cur_player_finished = True
                self.selected_piece = 0
