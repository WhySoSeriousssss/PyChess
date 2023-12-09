from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Signal


class MenuUI(QWidget):

    # signals
    self_play_signal = Signal()

    def __init__(self):
        super().__init__()

        # buttons
        btn_self_play = QPushButton('Self Play')
        btn_play_with_bot = QPushButton('Play With Bot')
        btn_play_online = QPushButton('Play Online')

        btn_self_play.clicked.connect(self.btn_self_play_clicked)
        btn_play_with_bot.clicked.connect(self.btn_play_with_bot_clicked)
        btn_play_online.clicked.connect(self.btn_play_online_clicked)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(btn_self_play)
        layout.addWidget(btn_play_with_bot)
        layout.addWidget(btn_play_online)
        self.setLayout(layout)

    def btn_self_play_clicked(self):
        self.self_play_signal.emit()

    def btn_play_with_bot_clicked(self):
        pass

    def btn_play_online_clicked(self):
        pass

