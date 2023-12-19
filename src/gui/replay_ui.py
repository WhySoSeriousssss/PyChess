from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PySide6.QtCore import Signal
from gui.chess_board_scene import ChessboardScene
from gui.chess_board_view import ChessboardView


class ReplayUI(QWidget):
    def __init__(self):
        super().__init__()

        self.replay_ui_widget = QWidget()
        self.replay_board_scene = ChessboardScene()
        self.replay_board_view = ChessboardView(self.replay_board_scene)

        self.replay_control_buttons = QWidget()
        self.btn_replay_to_beginning = QPushButton("<<")
        self.btn_replay_step_back = QPushButton("<")
        self.btn_replay_play = QPushButton("Play")
        self.btn_replay_pause = QPushButton("Pause")
        self.btn_replay_step_ahead = QPushButton(">")
        self.btn_replay_to_end = QPushButton(">>")

        self.btn_replay_to_beginning.clicked.connect(self.btn_replay_to_beginning_clicked)
        self.btn_replay_step_back.clicked.connect(self.btn_replay_step_back_clicked)
        self.btn_replay_play.clicked.connect(self.btn_replay_play_clicked)
        self.btn_replay_pause.clicked.connect(self.btn_replay_pause_clicked)
        self.btn_replay_step_ahead.clicked.connect(self.btn_replay_step_ahead_clicked)
        self.btn_replay_to_end.clicked.connect(self.btn_replay_to_end_clicked)
        
        btns_layout = QHBoxLayout()
        btns_layout.addWidget(self.btn_replay_to_beginning)
        btns_layout.addWidget(self.btn_replay_step_back)
        btns_layout.addWidget(self.btn_replay_play)
        btns_layout.addWidget(self.btn_replay_pause)
        btns_layout.addWidget(self.btn_replay_step_ahead)
        btns_layout.addWidget(self.btn_replay_to_end)
        self.replay_control_buttons.setLayout(btns_layout)

        layout = QVBoxLayout(self.replay_ui_widget)
        layout.addWidget(self.replay_control_buttons)
        layout.addWidget(self.replay_board_view)
        self.setLayout(layout)

    def set_replay_data(self, data):
        data

    def btn_replay_to_beginning_clicked(self):
        pass

    def btn_replay_step_back_clicked(self):
        pass

    def btn_replay_play_clicked(self):
        pass

    def btn_replay_pause_clicked(self):
        pass

    def btn_replay_step_ahead_clicked(self):
        pass

    def btn_replay_to_end_clicked(self):
        pass
