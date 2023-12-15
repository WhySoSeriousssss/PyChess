import os
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPoint, Signal
from game_core.board import *


ASSET_BOARD_PATH = "assets/board/board.png"
ASSET_PIECES_PATH = "assets/pieces/"
PIECES_FILE_NAMES = ["red_pawn", "red_cannon", "red_rook", "red_knight", "red_bishop", "red_advisor", "red_king",
                     "black_pawn", "black_cannon", "black_rook", "black_knight", "black_bishop", "black_advisor", "black_king"]

PIECE_SIZE = (50, 50)
PIECE_CLICKABLE_AREA = (40, 40)
BOARD_SIZE = (500, 450)
BOARD_OFFSET = (25, 25)
BOARD_SPACING = (50, 50)


class ChessPiece(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.row = 0
        self.col = 0
    
    def set_coord(self, coord):
        self.setPos(BOARD_OFFSET[1] + coord[1] * BOARD_SPACING[1] - PIECE_SIZE[1] // 2, 
                    BOARD_OFFSET[0] + coord[0] * BOARD_SPACING[0] - PIECE_SIZE[0] // 2)
        self.row = coord[0]
        self.col = coord[1]


class ChessboardScene(QGraphicsScene):
    board_clicked_signal = Signal(tuple)  # coord

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)
        # init board
        chessboard_pixmap = QPixmap(ASSET_BOARD_PATH).scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)
        self.chessboard_item = QGraphicsPixmapItem(chessboard_pixmap)
        self.addItem(self.chessboard_item)
        # init chess pieces
        self.pieces = []
        for piece_id in range(1, 33):
            piece_type = piece_id_to_type[piece_id - 1]
            piece_owner = piece_id_to_owner[piece_id - 1]
            piece_name = PIECES_FILE_NAMES[piece_owner * 7 + piece_type - 1]
            piece_pixmap = QPixmap(os.path.join(ASSET_PIECES_PATH, piece_name)).scaled(PIECE_SIZE[1], PIECE_SIZE[0], Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)
            piece_item = ChessPiece(piece_pixmap)
            self.pieces.append(piece_item)
        # keeps a copy of the board state
        self.board_state = [
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
        ]  # init board state
        # init the board UI
        for i in range(len(self.board_state)):
            for j in range(len(self.board_state[0])):
                piece_id = self.board_state[i][j]
                if piece_id == 0:
                    continue
                piece_item = self.pieces[piece_id - 1]
                piece_item.set_coord((i, j))
                self.addItem(piece_item)

    def update_board_ui(self, piece_id, new_coord):
        piece_to_move = self.pieces[piece_id - 1]
        # kill the orignal piece at the new coord
        new_coord_piece_id = self.board_state[new_coord[0]][new_coord[1]]
        if new_coord_piece_id != 0:
            self.pieces[new_coord_piece_id - 1].setVisible(False)
        # update the board state
        self.board_state[piece_to_move.row][piece_to_move.col] = 0
        self.board_state[new_coord[0]][new_coord[1]] = piece_id
        # move the piece to the new coord
        piece_to_move.set_coord(new_coord)
        
    def mousePressEvent(self, event):
        """
        handle the click event from the game board label, convert the clicked position to the board coordinate,
        and send the game_board_click signal
        """
        # transform the clicked position
        pos = QPoint(event.scenePos().y(), event.scenePos().x())
        pos = pos - QPoint(BOARD_OFFSET[0], BOARD_OFFSET[1])
        pos = pos + QPoint(PIECE_CLICKABLE_AREA[0] // 2, PIECE_CLICKABLE_AREA[1] // 2)
        # check if the clicked position is inside the valid area
        if (0 < pos.x() % BOARD_SPACING[0] < PIECE_CLICKABLE_AREA[0] \
                and 0 < pos.y() % BOARD_SPACING[1] < PIECE_CLICKABLE_AREA[1]):
            # convert click position to game board coordinate
            x_idx, y_idx = pos.x() // BOARD_SPACING[0], pos.y() // BOARD_SPACING[1]
            self.board_clicked_signal.emit((x_idx, y_idx))
