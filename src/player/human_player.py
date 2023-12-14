from typing import Optional
from PySide6.QtCore import QThread, Signal


class HumanPlayer:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.selected_piece = 0
        self.selected_coord = (0, 0)
        self.action_made = False
        
    def get_action(self, board):
        while not self.action_made:
            continue
        self.action_made = False
        return self.selected_piece, self.selected_coord

    def set_piece(self, piece_id):
        # print("HumanPlayer:handle_piece_selected()", QThread.currentThread)
        self.selected_piece = piece_id

    def set_coord(self, coord):
        # print("HumanPlayer:handle_coord_selected()", QThread.currentThread)
        self.selected_coord = coord
        self.action_made = True


class HumanPlayerThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
