import numpy as np
from enum import Enum

class Piece(Enum):
    SOLDIER     = 1  # 兵/卒
    CANNON      = 2  # 炮
    CHARIOT     = 3  # 车
    HORSE       = 4  # 马
    ELEPHANT    = 5  # 象
    ADVISOR     = 6  # 士
    GENERAL     = 7  # 帅/将


class Board:
    def __init__(self):
        self.height = 10
        self.width = 9
        self.cur_state = np.zeros((self.height, self.width), dtype=int)

    def init_board(self, start_player):
        self.cur_state = np.array([
            [-3, -4, -5, -6, -7, -6, -5, -4, -3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, -2, 0, 0, 0, 0, 0, -2, 0],
            [-1, 0, -1, 0, -1, 0, -1, 0, -1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 2, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 4, 5, 6, 7, 6, 5, 4, 3]
        ])
        self.cur_player = start_player
        self.start_player = start_player

    def move_piece(self):
        pass

    def game_finished(self):
        return False, -1
