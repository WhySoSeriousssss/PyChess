from PySide6.QtWidgets import QMainWindow
from gui.game_ui import GameUI
from gui.menu_ui import MenuUI
from core.gameplay import GameplayThread, GameMode


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
        self.game_ui = GameUI()

        # game thread
        self.gameplay_thread = GameplayThread(self)

        self.init_menu()

    def init_menu(self):
        self.setCentralWidget(self.menu_ui)

    def init_game_self_play(self):
        self.setCentralWidget(self.game_ui)
        
        # init the gameplay thread
        self.gameplay_thread.move_piece_signal.connect(self.update_gui)
        self.gameplay_thread.init_game(GameMode.SELF_PLAY, ["player1", "player2"], 0)
        
        # init game UI
        self.game_ui.render_board(self.gameplay_thread.board.cur_state)

        # start game loop
        self.gameplay_thread.start()

    def update_gui(self, value):
        # print(f"Updating GUI with value: {value}")
        pass

    def closeEvent(self, event):
        self.gameplay_thread.terminate()
        # self.gameplay_thread.quit()
        self.gameplay_thread.wait()
        event.accept()
