from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QPushButton
from gui.menu_ui import MenuUI
from gui.replay_ui import ReplayUI
from gui.chess_board_scene import ChessboardScene
from gui.chess_board_view import ChessboardView
from game_core.gameplay import GameplayThread, GameMode


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle("PyChess")
        self.resize(500, 600)   
        self.gameplay_thread = None
        # init menu     
        self.init_menu()

    def init_menu(self):
        menu_ui = MenuUI()
        menu_ui.start_game_signal.connect(self.start_game)
        menu_ui.watch_replay_signal.connect(self.watch_replay)
        self.setCentralWidget(menu_ui)

    def start_game(self, game_mode):
        # init game UI
        self.game_ui_widget = QWidget()
        self.board_scene = ChessboardScene()
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

    def watch_replay(self, replay_file):
        print(f"opened {replay_file}")
        # init replay UI
        self.replay_ui = ReplayUI(replay_file)
        self.setCentralWidget(self.replay_ui)

    def handle_self_player_finished(self, winner):
        self.gameplay_thread.terminate()
        self.gameplay_thread.wait()
        self.gameplay_thread.deleteLater()
        if winner == -1:
            QMessageBox.information(self, "Game Over", f"It's a tie!")
        else:
            QMessageBox.information(self, "Game Over", f"Player {winner} Won!")
        self.init_menu()

    def closeEvent(self, event):
        # TODO: "RuntimeError: Internal C++ object (GameplayThread) already deleted."
        if self.gameplay_thread:
            self.gameplay_thread.terminate()
            self.gameplay_thread.wait()
        event.accept()
