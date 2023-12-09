from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal, QPoint


class BoardLabel(QLabel):
    click_signal = Signal(QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_position = event.pos()
            self.click_signal.emit(click_position)

