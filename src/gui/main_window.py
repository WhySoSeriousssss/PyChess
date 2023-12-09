from PySide6.QtWidgets import QMainWindow
from gui.game_widget import GameWidget
from gui.menu_widget import MenuWidget
from core.gameplay import GameplayThread, GameMode


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle("PyChess")
        self.resize(1000, 1200)

        # menu widget
        self.menu_widget = MenuWidget()
        self.menu_widget.self_play_signal.connect(self.init_game_self_play)
        # game widget
        self.game_widget = GameWidget()

        # game thread
        self.gameplay_thread = GameplayThread(self)

        self.init_menu()

    def init_menu(self):
        self.setCentralWidget(self.menu_widget)

    def init_game_self_play(self):
        self.setCentralWidget(self.game_widget)
        
        # start the gameplay thread
        self.gameplay_thread.move_piece_signal.connect(self.update_gui)
        self.gameplay_thread.init_game(GameMode.SELF_PLAY, ["player1", "player2"], 0)
        self.gameplay_thread.start()

        self.game_widget.render_board(self.gameplay_thread.board.cur_state)

    def update_gui(self, value):
        print(f"Updating GUI with value: {value}")

    def closeEvent(self, event):
        self.gameplay_thread.terminate()
        # self.gameplay_thread.quit()
        self.gameplay_thread.wait()
        event.accept()
