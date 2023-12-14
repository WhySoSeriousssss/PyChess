from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Signal
from game_core.game_info import GameMode


class MenuUI(QWidget):

    # signals
    start_game_signal = Signal(int)

    def __init__(self):
        super().__init__()

        # buttons
        btn_self_play = QPushButton('Self Play')
        btn_play_with_bot = QPushButton('Play With Bot')
        btn_bot_combat = QPushButton('Bot Combat')
        btn_play_online = QPushButton('Play Online')

        btn_self_play.clicked.connect(self.btn_self_play_clicked)
        btn_play_with_bot.clicked.connect(self.btn_play_with_bot_clicked)
        btn_bot_combat.clicked.connect(self.btn_bot_combat_clicked)
        btn_play_online.clicked.connect(self.btn_play_online_clicked)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(btn_self_play)
        layout.addWidget(btn_play_with_bot)
        layout.addWidget(btn_bot_combat)
        layout.addWidget(btn_play_online)
        self.setLayout(layout)

    def btn_self_play_clicked(self):
        self.start_game_signal.emit(GameMode.SELF_PLAY.value)

    def btn_play_with_bot_clicked(self):
        self.start_game_signal.emit(GameMode.PLAY_WITH_BOT.value)

    def btn_bot_combat_clicked(self):
        self.start_game_signal.emit(GameMode.BOT_COMBAT.value)

    def btn_play_online_clicked(self):
        self.start_game_signal.emit(GameMode.SELF_PLAY.value)

