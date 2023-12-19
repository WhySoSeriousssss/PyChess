from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from game_core.game_info import GameMode


class MenuUI(QWidget):

    # signals
    start_game_signal = Signal(int)
    watch_replay_signal = Signal(str)

    def __init__(self):
        super().__init__()

        # buttons
        btn_self_play = QPushButton('Self Play')
        btn_play_with_bot = QPushButton('Play With Bot')
        btn_bot_combat = QPushButton('Bot Combat')
        btn_play_online = QPushButton('Play Online')
        btn_watch_replay = QPushButton('Watch Replay')

        btn_self_play.setMinimumHeight(80)
        btn_play_with_bot.setMinimumHeight(80)
        btn_bot_combat.setMinimumHeight(80)
        btn_play_online.setMinimumHeight(80)
        btn_watch_replay.setMinimumHeight(80)

        font = QFont()
        font.setPointSize(16)
        btn_self_play.setFont(font)
        btn_play_with_bot.setFont(font)
        btn_bot_combat.setFont(font)
        btn_play_online.setFont(font)
        btn_watch_replay.setFont(font)

        btn_self_play.clicked.connect(self.btn_self_play_clicked)
        btn_play_with_bot.clicked.connect(self.btn_play_with_bot_clicked)
        btn_bot_combat.clicked.connect(self.btn_bot_combat_clicked)
        btn_play_online.clicked.connect(self.btn_play_online_clicked)
        btn_watch_replay.clicked.connect(self.btn_watch_replay_clicked)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(btn_self_play)
        layout.addWidget(btn_play_with_bot)
        layout.addWidget(btn_bot_combat)
        layout.addWidget(btn_play_online)
        layout.addWidget(btn_watch_replay)
        self.setLayout(layout)

    def btn_self_play_clicked(self):
        self.start_game_signal.emit(GameMode.SELF_PLAY.value)

    def btn_play_with_bot_clicked(self):
        self.start_game_signal.emit(GameMode.PLAY_WITH_BOT.value)

    def btn_bot_combat_clicked(self):
        self.start_game_signal.emit(GameMode.BOT_COMBAT.value)

    def btn_play_online_clicked(self):
        self.start_game_signal.emit(GameMode.SELF_PLAY.value)

    def btn_watch_replay_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Replay File", "", "JSON Files(*.json)")
        self.watch_replay_signal.emit(file_name)
