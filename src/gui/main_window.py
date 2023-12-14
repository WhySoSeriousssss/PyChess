from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from gui.menu_ui import MenuUI
from gui.chess_board_scene import ChessboardScene
from gui.chess_board_view import ChessboardView
from game_core.gameplay import GameplayThread, GameMode


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle("PyChess")
        self.resize(1000, 1200)        
        self.init_menu()

    def init_menu(self):
        menu_ui = MenuUI()
        menu_ui.start_game_signal.connect(self.start_game)
        self.setCentralWidget(menu_ui)

    def start_game(self, game_mode):
        # init game UI
        self.game_ui_widget = QWidget()
        self.board_scene = ChessboardScene(902, 1002)
        self.board_view = ChessboardView(self.board_scene)

        layout = QVBoxLayout(self.game_ui_widget)
        layout.addWidget(self.board_view)
        self.setCentralWidget(self.game_ui_widget)

        # init gameplay thread
        self.gameplay_thread = GameplayThread(self)
        self.gameplay_thread.player_moved_signal.connect(self.board_scene.update_board_ui)
        self.gameplay_thread.game_finished_signal.connect(self.handle_self_player_finished)
        if game_mode != GameMode.BOT_COMBAT:
            self.board_scene.board_clicked_signal.connect(self.gameplay_thread.handle_user_input)
        self.gameplay_thread.init_game(game_mode, 0)

        # start game loop
        self.gameplay_thread.start()

    def init_game_AI_vs_AI(self):
        pass

    def handle_self_player_finished(self, winner):
        self.gameplay_thread.terminate()
        self.gameplay_thread.wait()
        self.gameplay_thread.deleteLater()
        QMessageBox.information(self, "Game Over", f"Player {winner} Won!")
        self.init_menu()

    def closeEvent(self, event):
        # TODO: "RuntimeError: Internal C++ object (GameplayThread) already deleted."
        self.gameplay_thread.terminate()
        self.gameplay_thread.wait()
        event.accept()
