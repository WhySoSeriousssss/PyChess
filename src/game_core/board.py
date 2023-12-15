import numpy as np
from enum import Enum
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

piece_id_to_chinese_name = ["車", "馬", "象", "士", "将", "士", "象", "馬", "車", "炮", "炮", "卒", "卒", "卒", "卒", "卒",
                            "兵", "兵", "兵", "兵", "兵", "炮", "炮", "車", "馬", "相", "仕", "帅", "仕", "相", "馬", "車"]

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
        self.players_in_check = [False, False]
        self.update_availables(self.cur_state)

    def update_availables(self, board_state):
        self.availables.clear()
        # Get the coordinates of non-zero elements
        pieces_coords = np.transpose(np.nonzero(board_state)).tolist()
        for coord in pieces_coords:
            new_coords = []
            piece_id = board_state[tuple(coord)]
            piece_type = piece_id_to_type[piece_id - 1]
            piece_owner = piece_id_to_owner[piece_id - 1]

            if piece_type == Piece.SOLDIER.value:
                if piece_owner == 0:  # red
                    new_coords += [(bound(coord[0] - 1, 0, self.height - 1), coord[1])] # forward
                    if coord[0] < 5:  # has crossed the river
                        new_coords += [
                            (coord[0], bound(coord[1] - 1, 0, self.width - 1)),  # left
                            (coord[0], bound(coord[1] + 1, 0, self.width - 1))  # right
                        ]
                else:  # black
                    new_coords += [(bound(coord[0] + 1, 0, self.height - 1), coord[1])]  # forward
                    if coord[0] > 4:  # has crossed the river
                        new_coords += [
                            (coord[0], bound(coord[1] - 1, 0, self.width - 1)),  # left
                            (coord[0], bound(coord[1] + 1, 0, self.width - 1))  # right
                        ]

            elif piece_type == Piece.CANNON.value:
                # left
                attack_mode = False
                for i in range(coord[1] - 1, -1, -1):
                    if not attack_mode:
                        if board_state[coord[0], i] == 0:
                            new_coords.append((coord[0], i))
                        else:
                            attack_mode = True
                    else:
                        if board_state[coord[0], i] != 0:
                            if piece_id_to_owner[board_state[coord[0], i] - 1] != piece_owner:
                                new_coords.append((coord[0], i))
                            break
                # right
                attack_mode = False
                for i in range(coord[1] + 1, 9, 1):
                    if not attack_mode:
                        if board_state[coord[0], i] == 0:
                            new_coords.append((coord[0], i))
                        else:
                            attack_mode = True
                    else:
                        if board_state[coord[0], i] != 0:
                            if piece_id_to_owner[board_state[coord[0], i] - 1] != piece_owner:
                                new_coords.append((coord[0], i))
                            break
                # up
                attack_mode = False
                for i in range(coord[0] - 1, -1, -1):
                    if not attack_mode:
                        if board_state[i, coord[1]] == 0:
                            new_coords.append((i, coord[1]))
                        else:
                            attack_mode = True
                    else:
                        if board_state[i, coord[1]] != 0:
                            if piece_id_to_owner[board_state[i, coord[1]] - 1] != piece_owner:
                                new_coords.append((i, coord[1]))
                            break
                # down
                attack_mode = False
                for i in range(coord[0] + 1, 10, 1):
                    if not attack_mode:
                        if board_state[i, coord[1]] == 0:
                            new_coords.append((i, coord[1]))
                        else:
                            attack_mode = True
                    else:
                        if board_state[i, coord[1]] != 0:
                            if piece_id_to_owner[board_state[i, coord[1]] - 1] != piece_owner:
                                new_coords.append((i, coord[1]))
                            break

            elif piece_type == Piece.CHARIOT.value:
                # left
                for i in range(coord[1] - 1, -1, -1):
                    if board_state[coord[0], i] == 0:
                        new_coords.append((coord[0], i))
                    else:
                        if piece_id_to_owner[board_state[coord[0], i] - 1] != piece_owner:
                            new_coords.append((coord[0], i))
                        break
                # right
                for i in range(coord[1] + 1, 9, 1):
                    if board_state[coord[0], i] == 0:
                        new_coords.append((coord[0], i))
                    else:
                        if piece_id_to_owner[board_state[coord[0], i] - 1] != piece_owner:
                            new_coords.append((coord[0], i))
                        break
                # up
                for i in range(coord[0] - 1, -1, -1):
                    if board_state[i, coord[1]] == 0:
                        new_coords.append((i, coord[1]))
                    else:
                        if piece_id_to_owner[board_state[i, coord[1]] - 1] != piece_owner:
                            new_coords.append((i, coord[1]))
                        break
                # down
                for i in range(coord[0] + 1, 10, 1):
                    if board_state[i, coord[1]] == 0:
                        new_coords.append((i, coord[1]))
                    else:
                        if piece_id_to_owner[board_state[i, coord[1]] - 1] != piece_owner:
                            new_coords.append((i, coord[1]))
                        break

            elif piece_type == Piece.HORSE.value:
                if coord[0] > 0 and coord[1] > 1 and board_state[coord[0], coord[1] - 1] == 0:
                    new_coords.append((coord[0] - 1, coord[1] - 2)) # up-left 1
                if coord[0] > 1 and coord[1] > 0 and board_state[coord[0] - 1, coord[1]] == 0:
                    new_coords.append((coord[0] - 2, coord[1] - 1)) # up-left 2
                if coord[0] > 0 and coord[1] < 7 and board_state[coord[0], coord[1] + 1] == 0:
                    new_coords.append((coord[0] - 1, coord[1] + 2)) # up-right 1
                if coord[0] > 1 and coord[1] < 8 and board_state[coord[0] - 1, coord[1]] == 0:
                    new_coords.append((coord[0] - 2, coord[1] + 1)) # up-right 2
                if coord[0] < 9 and coord[1] > 1 and board_state[coord[0], coord[1] - 1] == 0:
                    new_coords.append((coord[0] + 1, coord[1] - 2)) # down-left 1
                if coord[0] < 8 and coord[1] > 0 and board_state[coord[0] + 1, coord[1]] == 0:
                    new_coords.append((coord[0] + 2, coord[1] - 1)) # down-left 2
                if coord[0] < 9 and coord[1] < 7 and board_state[coord[0], coord[1] + 1] == 0:
                    new_coords.append((coord[0] + 1, coord[1] + 2)) # down-right 1
                if coord[0] < 8 and coord[1] < 8 and board_state[coord[0] + 1, coord[1]] == 0:
                    new_coords.append((coord[0] + 2, coord[1] + 1)) # down-right 2

            elif piece_type == Piece.ELEPHANT.value:
                if piece_owner == 0:
                    if coord[0] > 6 and coord[1] > 0 and board_state[coord[0] - 1, coord[1] - 1] == 0:
                        new_coords.append((coord[0] - 2, coord[1] - 2))  # up-left
                    if coord[0] > 6 and coord[1] < 8 and board_state[coord[0] - 1, coord[1] + 1] == 0:
                        new_coords.append((coord[0] - 2, coord[1] + 2))  # up-right
                    if coord[0] < 8 and coord[1] > 0 and board_state[coord[0] + 1, coord[1] - 1] == 0:
                        new_coords.append((coord[0] + 2, coord[1] - 2))  # down-left
                    if coord[0] < 8 and coord[1] < 8 and board_state[coord[0] + 1, coord[1] + 1] == 0:
                        new_coords.append((coord[0] + 2, coord[1] + 2))  # down-right
                else:
                    if coord[0] > 1 and coord[1] > 0 and board_state[coord[0] - 1, coord[1] - 1] == 0:
                        new_coords.append((coord[0] - 2, coord[1] - 2))  # up-left
                    if coord[0] > 1 and coord[1] < 8 and board_state[coord[0] - 1, coord[1] + 1] == 0:
                        new_coords.append((coord[0] - 2, coord[1] + 2))  # up-right
                    if coord[0] < 3 and coord[1] > 0 and board_state[coord[0] + 1, coord[1] - 1] == 0:
                        new_coords.append((coord[0] + 2, coord[1] - 2))  # down-left
                    if coord[0] < 3 and coord[1] < 8 and board_state[coord[0] + 1, coord[1] + 1] == 0:
                        new_coords.append((coord[0] + 2, coord[1] + 2))  # down-right
            
            elif piece_type == Piece.ADVISOR.value:
                if piece_owner == 0:
                    if coord[0] > 7 and coord[1] > 3:
                        new_coords.append((coord[0] - 1, coord[1] - 1))  # up-left
                    if coord[0] > 7 and coord[1] < 5:
                        new_coords.append((coord[0] - 1, coord[1] + 1))  # up-right
                    if coord[0] < 9 and coord[1] > 3:
                        new_coords.append((coord[0] + 1, coord[1] - 1))  # down-left
                    if coord[0] < 9 and coord[1] < 5:
                        new_coords.append((coord[0] + 1, coord[1] + 1))  # down-right
                else:
                    if coord[0] > 0 and coord[1] > 3:
                        new_coords.append((coord[0] - 1, coord[1] - 1))  # up-left
                    if coord[0] > 0 and coord[1] < 5:
                        new_coords.append((coord[0] - 1, coord[1] + 1))  # up-right
                    if coord[0] < 2 and coord[1] > 3:
                        new_coords.append((coord[0] + 1, coord[1] - 1))  # down-left
                    if coord[0] < 2 and coord[1] < 5:
                        new_coords.append((coord[0] + 1, coord[1] + 1))  # down-right
            
            elif piece_type == Piece.GENERAL.value:
                if piece_owner == 0:
                    if coord[0] > 7:
                        new_coords.append((coord[0] - 1, coord[1]))  # forward
                    if coord[0] < 9:
                        new_coords.append((coord[0] + 1, coord[1]))  # backward
                    if coord[1] > 3:
                        new_coords.append((coord[0], coord[1] - 1))  # left
                    if coord[1] < 5:
                        new_coords.append((coord[0], coord[1] + 1))  # right
                else:
                    if coord[0] > 0:
                        new_coords.append((coord[0] - 1, coord[1]))  # backward
                    if coord[0] < 2:
                        new_coords.append((coord[0] + 1, coord[1]))  # forward
                    if coord[1] > 3:
                        new_coords.append((coord[0], coord[1] - 1))  # left
                    if coord[1] < 5:
                        new_coords.append((coord[0], coord[1] + 1))  # right

            for new_coord in new_coords:
                if (board_state[new_coord] == 0 or piece_id_to_owner[board_state[new_coord] - 1] != piece_owner) \
                        and coord != new_coord and self.check_move_valid(piece_owner, piece_id, new_coord):
                    self.availables[piece_id].append(new_coord)

    def check_move_valid(self, player, piece_id, coord):
        """
        Check if a move by the player will cause himself be in check
        """
        state = self.cur_state.copy()
        state[np.where(self.cur_state == piece_id)] = 0
        state[coord] = piece_id
        return not self.check_generals_meet(state) \
            # and not self.check_player_in_check(player, state) 

    def check_generals_meet(self, board_state):
        """
        Check if 2 generals are in the same column and there are no other pieces in between
        """
        red_general_pos = np.where(board_state == 28)
        if not red_general_pos:
            return False
        black_general_pos = np.where(board_state == 28)
        if not black_general_pos:
            return False
        if red_general_pos[1][0] != black_general_pos[1][0]:  # 2 generals not in the same column
            return False
        if np.sum(board_state[:, red_general_pos[1][0]]) == 33:  # only 2 generals in the same column
            return True
        return False
    
    def check_player_in_check(self, player, board_state):
        """
        Check if a player is in check
        """
        if player == 0:
            general_piece_id = 28
        else:
            general_piece_id = 5
        general_coord = tuple(np.transpose(np.where(board_state == general_piece_id))[0])
        # check if the player's general is in the attack range of any opponent's piece
        for piece_id, moves in self.availables.items():
            if piece_id_to_owner[piece_id - 1] == 1 - player:
                if general_coord in moves:
                    return True
        return False
    
    def check_player_checkmate(self, player, board_state):
        """
        Check if a player is checkmate
        """
        # TODO: implement
        pass

    def check_stalement(self, player):
        """
        Check if a player has no legal move
        """
        for piece_id, moves in self.availables.items():
            if piece_id_to_owner[piece_id - 1] == player:
                if len(moves) > 0:
                    return False
        return True

    def check_move_available(self, piece_id, coord):
        """
        Check if a move is in the availables
        """
        valid = piece_id in self.availables.keys() \
            and coord in self.availables[piece_id]
        # print("validity", piece_id, coord, valid, self.availables[piece_id])
        return valid
    
    def move_piece(self, piece_id, coord):
        self.cur_state[np.where(self.cur_state == piece_id)] = 0
        self.cur_state[coord] = piece_id
        self.update_availables(self.cur_state)
        self.cur_player = 1 - self.cur_player  # switch the player

    def game_finished(self):
        p1_in_check = self.check_player_in_check(0, self.cur_state)
        p2_in_check = self.check_player_in_check(1, self.cur_state)
        # print(f"Player1 checked: {p1_in_check}, Player2 checked: {p2_in_check}")
        # check p1
        if p1_in_check and (self.players_in_check[0] or self.cur_player == 1):
            return True, 1
        self.players_in_check[0] = p1_in_check
        # check p2
        if p2_in_check and (self.players_in_check[1] or self.cur_player == 0):
            return True, 0
        self.players_in_check[1] = p2_in_check

        return False, -1

    def coord_to_idx(self, coord):
        return coord[0] * self.width + coord[1]
    