import numpy as np
from enum import Enum
from PySide6.QtCore import QPoint
from collections import defaultdict
from utils.math import bound


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
        self.availables = defaultdict(list)

    def init_board(self, start_player):
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
        self.update_availables()

    def update_availables(self):
        self.availables.clear()
        # Get the coordinates of non-zero elements
        pieces_coords = np.transpose(np.nonzero(self.cur_state)).tolist()
        for coord in pieces_coords:
            piece_id = self.cur_state[tuple(coord)]
            piece_type = piece_id_to_type[piece_id - 1]
            piece_owner = piece_id_to_owner[piece_id - 1]

            if piece_type == Piece.SOLDIER.value:
                if piece_owner == 0:
                    if coord[1] in [5, 6]:
                        new_coords = [
                            QPoint(bound(coord[0] - 1, 0, self.height - 1), coord[1]),  # forward
                        ]
                    else:
                        new_coords = [
                            QPoint(bound(coord[0] - 1, 0, self.height - 1), coord[1]),  # forward
                            QPoint(coord[0], bound(coord[1] - 1, 0, self.width - 1)),  # left
                            QPoint(coord[0], bound(coord[1] + 1, 0, self.width - 1))  # right
                        ]
                else:
                    pass
            elif piece_type == Piece.CANNON.value:
                pass
            elif piece_type == Piece.CHARIOT.value:
                pass
            elif piece_type == Piece.HORSE.value:
                pass
            elif piece_type == Piece.ELEPHANT.value:
                if piece_owner == 0:
                    pass
                else:
                    pass
            elif piece_type == Piece.ADVISOR.value:
                if piece_owner == 0:
                    pass
                else:
                    pass
            elif piece_type == Piece.GENERAL.value:
                if piece_owner == 0:
                    pass
                else:
                    pass

    def check_move_validity(self, piece_id, coord):
        valid = piece_id in self.availables.keys() \
            and self.coord_to_idx(coord) in self.availables[piece_id]
        return valid

    def move_piece(self, piece_id, coord: QPoint):
        self.cur_state[np.where(self.cur_state == piece_id)] = 0
        self.cur_state[coord.x(), coord.y()] = piece_id
        self.update_availables()

    def game_finished(self):
        return False, -1

    def coord_to_idx(self, coord: QPoint):
        return coord.x() * self.width + coord.y()
    