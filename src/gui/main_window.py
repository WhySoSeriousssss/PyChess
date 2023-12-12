from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from gui.menu_ui import MenuUI
from gui.chess_board_scene import ChessboardScene
from gui.chess_board_view import ChessboardView
from core.gameplay import GameplayThread, GameMode
import time


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle("PyChess")
        self.resize(1000, 1200)

        # menu widget
        self.menu_ui = MenuUI()
        self.menu_ui.self_play_signal.connect(self.init_game_self_play)
        
        # game widget
        self.game_ui_widget = QWidget()
        self.board_scene = ChessboardScene(902, 1002)
        self.board_view = ChessboardView(self.board_scene)

        layout = QVBoxLayout(self.game_ui_widget)
        layout.addWidget(self.board_view)

        # game thread
        self.gameplay_thread = GameplayThread(self)

        self.init_menu()

    def init_menu(self):
        self.setCentralWidget(self.menu_ui)

    def init_game_self_play(self):
        self.setCentralWidget(self.game_ui_widget)
        
        # init the gameplay thread
        self.gameplay_thread.player_moved_signal.connect(self.board_scene.update_board_ui)
        self.gameplay_thread.init_game(GameMode.SELF_PLAY, ["player1", "player2"], 0)
        self.board_scene.board_clicked_signal.connect(self.gameplay_thread.handle_user_input)
        
        # start game loop
        self.gameplay_thread.start()

    def closeEvent(self, event):
        self.gameplay_thread.terminate()
        # self.gameplay_thread.quit()
        self.gameplay_thread.wait()
        event.accept()
