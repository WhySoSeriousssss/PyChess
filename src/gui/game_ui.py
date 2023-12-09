import cv2
import numpy as np
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QPoint, Signal
from utils.image_process import paste
from utils.math import bound
from gui.board_label import BoardLabel


piece_assets_path = "assets/pieces/"
black_piece_assets_names = ["black_pawn", "black_cannon", "black_rook", "black_knight", "black_bishop", "black_advisor", "black_king"]
red_piece_assets_names = ["red_pawn", "red_cannon", "red_rook", "red_knight", "red_bishop", "red_advisor", "red_king"]
board_asset_path = "assets/board/xiangqi_gmchess_wood.png"

class GameUI(QWidget):
    game_board_click_signal = Signal(QPoint)

    def __init__(self):
        super().__init__()

        # geo info
        self.piece_size = (100, 100)
        self.board_size = (1002, 902)
        self.board_offset = (51, 51)
        self.board_spacing = (100, 100)

        # Game Board
        self.lbl_game_board = BoardLabel()
        self.lbl_game_board.click_signal.connect(self.handle_board_label_clicked)
        self.lbl_game_board.setScaledContents(True)
        self.lbl_game_board.setFixedSize(self.board_size[1], self.board_size[0])

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_game_board)
        self.setLayout(layout)

        # read empty board image (as numpy array)
        self.empty_board_img = cv2.imread(board_asset_path, cv2.IMREAD_UNCHANGED)
        # read piece images (as numpy array)
        self.red_piece_imgs = [cv2.resize(cv2.imread(piece_assets_path + path + '.png', cv2.IMREAD_UNCHANGED), self.piece_size) 
                               for path in red_piece_assets_names]
        self.black_piece_imgs = [cv2.resize(cv2.imread(piece_assets_path + path + '.png', cv2.IMREAD_UNCHANGED), self.piece_size) 
                                 for path in black_piece_assets_names]
                
    def render_board(self, board_state):
        """
        Render the board given the state
        """
        # Get the coordinates of non-zero elements
        pieces_coords = np.nonzero(board_state)

        # overlay each piece's image onto the board image
        board_img = self.empty_board_img.copy()

        for coord in list(zip(pieces_coords[0], pieces_coords[1])):
            piece_idx = board_state[coord]
            if piece_idx > 0:  # red pieces
                piece_img = self.red_piece_imgs[piece_idx - 1]
            else:  # black pieces
                piece_img = self.black_piece_imgs[-piece_idx - 1]
        
            paste(board_img, piece_img, (self.board_offset[0]+coord[0]*self.board_spacing[0]-self.piece_size[0]//2, 
                                         self.board_offset[1]+coord[1]*self.board_spacing[1]-self.piece_size[1]//2))

        # convert to QImage
        board_img = np.ascontiguousarray(board_img[:, :, :3])
        board_img = cv2.cvtColor(board_img, cv2.COLOR_BGR2RGB)
        height, width, channel = board_img.shape
        bytes_per_line = 3 * width
        qimage = QImage(board_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
         # render the board label
        self.lbl_game_board.setPixmap(QPixmap.fromImage(qimage))

    def handle_board_label_clicked(self, pos: QPoint):
        """
        handle the click event from the game board label, convert the clicked position to the board coordinate,
        and send the game_board_click signal
        """
        piece_clickable_range = (80, 80)
        # transform the clicked position
        pos = QPoint(pos.y(), pos.x())
        pos = pos - QPoint(self.board_offset[0], self.board_offset[1])
        pos = pos + QPoint(piece_clickable_range[0] // 2, piece_clickable_range[1] // 2)
        # check if the clicked position is inside the valid area
        if (0 < pos.x() % self.board_spacing[0] < piece_clickable_range[0] \
                and 0 < pos.y() % self.board_spacing[1] < piece_clickable_range[1]):
            # convert click position to game board coordinate
            x_idx, y_idx = pos.x() // self.board_spacing[0], pos.y() // self.board_spacing[1]
            self.game_board_click_signal.emit(QPoint(x_idx, y_idx))

