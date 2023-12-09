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

piece_id_to_type = [3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 2, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3]

piece_id_to_owner = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 0: red, 1: black

class Board:
    def __init__(self):
        self.height = 10
        self.width = 9
        self.cur_state = np.zeros((self.height, self.width), dtype=int)

    def init_board(self, start_player):
        # self.cur_state = np.array([
        #     [-3, -4, -5, -6, -7, -6, -5, -4, -3],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, -2, 0, 0, 0, 0, 0, -2, 0],
        #     [-1, 0, -1, 0, -1, 0, -1, 0, -1],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [1, 0, 1, 0, 1, 0, 1, 0, 1],
        #     [0, 2, 0, 0, 0, 0, 0, 2, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [3, 4, 5, 6, 7, 6, 5, 4, 3]
        # ])
        self.cur_state = np.array([
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 10, 0, 0, 0, 0, 0, 11, 0],
            [12, 0, 13, 0, 14, 0, 15, 0, 16],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [17, 0, 18, 0, 19, 0, 20, 0, 21],
            [0, 22, 0, 0, 0, 0, 0, 23, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [24, 25, 26, 27, 28, 29, 30, 31, 32]
        ])
        self.cur_player = start_player
        self.start_player = start_player

    def check_move_valid(self, piece_idx, coord):
        return True

    def move_piece(self, piece_idx, coord):
        pass

    def game_finished(self):
        return False, -1
