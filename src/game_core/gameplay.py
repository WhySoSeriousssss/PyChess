import json
from datetime import datetime
from PySide6.QtCore import QThread, Signal
from game_core.board import *
from game_core.game_info import GameMode
from player.human_player import HumanPlayer
from player.mcts_player import MCTSPlayer


class GameplayThread(QThread):
    player_moved_signal = Signal(int, tuple)  # piece_id, coord
    game_finished_signal = Signal(int)  # winner

    def init_game(self, game_mode, start_player=0):
        if game_mode == GameMode.SELF_PLAY.value:
            self.players = [HumanPlayer(0, "gg"), HumanPlayer(1, "mm")]
        elif game_mode == GameMode.PLAY_WITH_BOT.value:
            self.players = [HumanPlayer(0, "gg"), MCTSPlayer(1, "bot1", n_simulations=100)]
        elif game_mode == GameMode.BOT_COMBAT.value:
            self.players = [MCTSPlayer(0, "bot1", n_simulations=100), MCTSPlayer(1, "bot2", n_simulations=100)]

        self.start_player_id = start_player
        self.cur_player_id = start_player
        self.selected_piece = 0  # the piece the current player selected
        self.board = Board()
        self.board.init_board(self.start_player_id)

    def run(self):
        while True:
            player_in_turn = self.players[self.cur_player_id]
            piece_id, coord = player_in_turn.get_action(self.board, self.cur_player_id)  # player take action
            print(f"[GameplayThread]: Player \"{player_in_turn.name}\" moved {piece_id_to_chinese_name[piece_id-1]}({piece_id}) to {coord}")
            self.board.move_piece(piece_id, coord)  # update board state
            self.player_moved_signal.emit(piece_id, coord)  # update UI
            game_finished, winner = self.board.game_finished()  # check game finished
            if game_finished:
                break
            self.cur_player_id = 1 - self.cur_player_id  # switch the player
        # save the replay
        cur_time = datetime.now()
        formatted_time = cur_time.strftime("%Y%m%d-%H%M")
        self.save_replay(f"replays/{formatted_time}.json")
        # send game finished signal
        self.game_finished_signal.emit(winner)

    def handle_user_input(self, coord):
        piece_id = self.board.cur_state[coord]
        # first input: piece
        if self.selected_piece == 0:
            # player selected his own piece
            if piece_id != 0 and piece_id_to_owner[piece_id - 1] == self.cur_player_id:
                self.selected_piece = piece_id
                self.players[self.cur_player_id].set_piece(piece_id)
                print(f"[GameplayThread]: Player \"{self.players[self.cur_player_id].name}\" selected {piece_id_to_chinese_name[self.selected_piece-1]}({self.selected_piece}). Availables:{self.board.availables[self.selected_piece]}")
        # second input: coord
        else:
            # player selected his own piece
            if piece_id != 0 and piece_id_to_owner[piece_id - 1] == self.cur_player_id:
                # change selected piece
                self.selected_piece = piece_id
                self.players[self.cur_player_id].set_piece(piece_id)
                print(f"[GameplayThread]: Player \"{self.players[self.cur_player_id].name}\" selected {piece_id_to_chinese_name[self.selected_piece-1]}({self.selected_piece}). Availables:{self.board.availables[self.selected_piece]}")
            # player select a coord, check valid move
            elif self.board.check_move_available(self.selected_piece, coord):
                # make the move
                self.players[self.cur_player_id].set_coord(coord)
                # reset variables
                self.selected_piece = 0

    def save_replay(self, file_path):
        data = {}
        data['steps'] = []
        for move in self.board.all_moves:
            data['steps'].append([int(move[0]), [int(move[1][0]), int(move[1][1])]])
        with open(file_path, 'w') as f:
            json.dump(data, f)
