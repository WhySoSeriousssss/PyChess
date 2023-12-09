import cv2
import numpy as np
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap, QImage
from utils.image_process import paste


piece_assets_path = "assets/pieces/"
black_piece_assets_names = ["black_pawn", "black_cannon", "black_rook", "black_knight", "black_bishop", "black_advisor", "black_king"]
red_piece_assets_names = ["red_pawn", "red_cannon", "red_rook", "red_knight", "red_bishop", "red_advisor", "red_king"]
board_asset_path = "assets/board/xiangqi_gmchess_wood.png"

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Game Board
        self.lbl_game_board = QLabel()
        self.lbl_game_board.setScaledContents(True)
        self.lbl_game_board.setFixedSize(902, 1002)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_game_board)
        self.setLayout(layout)

        # board geo info
        self.board_size = ()
        self.piece_size = (100, 100)
        self.board_offset = (51, 51)
        self.board_spacing = (100, 100)
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
