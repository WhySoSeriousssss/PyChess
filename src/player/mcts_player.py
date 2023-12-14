import random
import time
from PySide6.QtCore import QThread, Signal
from game_core.board import piece_id_to_owner


class MCTSPlayer:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name

    def get_action(self, board):
        time.sleep(1)
        legal_moves = board.availables
        piece_id = random.choice([piece_id for piece_id in legal_moves.keys() if piece_id_to_owner[piece_id - 1] == self.player_id])
        coord = random.choice(legal_moves[piece_id])
        return piece_id, coord