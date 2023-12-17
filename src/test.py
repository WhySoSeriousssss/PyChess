import numpy as np
from game_core.board import Board


board = Board()
board.init_board(0)
print(board.cur_state)

print(board.encode_move(24, (0, 9)))
print(board.decode_move(105, 1))

# for pid in range(2):
#     for move in range(192):
#         piece_id, coord = board.decode_move(move, pid)
#         move_ = board.encode_move(piece_id, coord)
#         if move != move_:
#             print(move)

# p1_availables = board.get_player_encoded_availables(0)
# print(np.where(np.array(p1_availables) > 0))

# p2_availables = board.get_player_encoded_availables(1)
# print(np.where(np.array(p2_availables) > 0))