import json
import numpy as np
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PySide6.QtCore import QTimer, Qt
from gui.chess_board_scene import ChessboardScene
from gui.chess_board_view import ChessboardView


class ReplayUI(QWidget):
    def __init__(self, replay_file):
        super().__init__()

        # widgets
        self.replay_board_scene = ChessboardScene()
        self.replay_board_view = ChessboardView(self.replay_board_scene)

        # buttons
        self.replay_control_buttons = QWidget()
        self.btn_replay_to_beginning = QPushButton("<<")
        self.btn_replay_step_back = QPushButton("<")
        self.btn_replay_play_pause = QPushButton("Play")
        self.btn_replay_play_pause.setCheckable(True)
        self.btn_replay_step_ahead = QPushButton(">")
        self.btn_replay_to_end = QPushButton(">>")
        # actions
        self.btn_replay_to_beginning.clicked.connect(self.btn_replay_to_beginning_clicked)
        self.btn_replay_step_back.clicked.connect(self.btn_replay_step_back_clicked)
        self.btn_replay_play_pause.clicked.connect(self.btn_replay_play_pause_clicked)
        self.btn_replay_step_ahead.clicked.connect(self.btn_replay_step_ahead_clicked)
        self.btn_replay_to_end.clicked.connect(self.btn_replay_to_end_clicked)
        # buttons layout
        btns_layout = QHBoxLayout()
        btns_layout.setContentsMargins(0, 0, 0, 0)
        btns_layout.addWidget(self.btn_replay_to_beginning)
        btns_layout.addWidget(self.btn_replay_step_back)
        btns_layout.addWidget(self.btn_replay_play_pause)
        btns_layout.addWidget(self.btn_replay_step_ahead)
        btns_layout.addWidget(self.btn_replay_to_end)
        self.replay_control_buttons.setLayout(btns_layout)

        # slider area
        self.slider_area = QWidget()
        self.slider = QSlider(Qt.Horizontal)
        self.step_label = QLabel()
        self.step_label.setMinimumWidth(60)
        # actions
        self.slider.sliderMoved.connect(self.set_cur_step)
        # layout
        slider_area_layout = QHBoxLayout()
        slider_area_layout.setContentsMargins(0, 0, 0, 0)
        slider_area_layout.addWidget(self.slider)
        slider_area_layout.addWidget(self.step_label)
        self.slider_area.setLayout(slider_area_layout)
        
        # overall layout
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.addWidget(self.replay_control_buttons)
        layout.addWidget(self.slider_area)
        layout.addWidget(self.replay_board_view)
        self.setLayout(layout)

        # timer
        self.autoplay_timer = QTimer(self)
        self.autoplay_timer.timeout.connect(self.btn_replay_step_ahead_clicked)
        self.autoplay_speed = 1.0
        self.autoplay_timer.setInterval(int(1000 / self.autoplay_speed))

        # read replay file
        self.read_replay_file(replay_file)

    def read_replay_file(self, replay_file):
        with open(replay_file, 'r') as file:
            # Load the JSON data
            data = json.load(file)
        self.steps = data['steps']
        self.cur_step = 0
        self.board_states = [np.array([
            [32, 31, 30, 29, 28, 27, 26, 25, 24],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 23, 0, 0, 0, 0, 0, 22, 0],
            [21, 0, 20, 0, 19, 0, 18, 0, 17],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 2, 0, 3, 0, 4, 0, 5],
            [0, 6, 0, 0, 0, 0, 0, 7, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 9, 10, 11, 12, 13, 14, 15, 16]
        ])]
        # record all board states
        for step in self.steps:
            piece_id, coord = step
            next_board_state = self.board_states[-1].copy()
            next_board_state[np.where(next_board_state == piece_id)] = 0
            next_board_state[tuple(coord)] = piece_id
            self.board_states.append(next_board_state)
        # init UI
        self.slider.setRange(0, len(self.steps))
        self.step_label.setText(f"{self.cur_step}/{len(self.steps)}")

    def set_cur_step(self, value):
        if value < 0 or value > len(self.steps):
            return
        self.cur_step = value
        self.replay_board_scene.set_board_state(self.board_states[self.cur_step])
        self.step_label.setText(f"{self.cur_step}/{len(self.steps)}")
        self.slider.setValue(self.cur_step)

    def btn_replay_to_beginning_clicked(self):
        self.set_cur_step(0)

    def btn_replay_step_back_clicked(self):
        self.set_cur_step(self.cur_step - 1)

    def btn_replay_play_pause_clicked(self):
        if self.btn_replay_play_pause.isChecked():
            self.btn_replay_play_pause.setText("Pause")
            self.autoplay_timer.start()
        else:
            self.btn_replay_play_pause.setText("Play")
            self.autoplay_timer.stop()

    def btn_replay_step_ahead_clicked(self):
        self.set_cur_step(self.cur_step + 1)
        # check auto-replay finished
        if self.autoplay_timer.isActive() and self.cur_step >= len(self.steps):
            self.btn_replay_play_pause.setText("Play")
            self.btn_replay_play_pause.setChecked(False)
            self.autoplay_timer.stop()

    def btn_replay_to_end_clicked(self):
        self.set_cur_step(len(self.steps))
