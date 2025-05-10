import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from knight_fight1 import Ui_window
from logic import Game

class GameApp(QMainWindow):
    '''Main window game is dispalyed in'''

    def __init__(self):
        '''initializes GUi interface and connects all buttons with code'''
        super().__init__()
        self.ui = Ui_window()
        self.ui.setupUi(self)
        self.game = Game(self.ui)
        self.selected_weapons = []

        self.ui.Axe_button.clicked.connect(lambda: self.pick_weapon('Axe'))
        self.ui.Sword_button.clicked.connect(lambda: self.pick_weapon('Sword'))
        self.ui.Spear_button.clicked.connect(lambda: self.pick_weapon('Spear'))
        self.ui.Dagger_button.clicked.connect(lambda: self.pick_weapon('Dagger'))
        self.ui.Begin_button.clicked.connect(self.begin_game)

        self.ui.Light_button.clicked.connect(lambda: self.game.player_attack('light'))
        self.ui.Heavy_button.clicked.connect(lambda: self.game.player_attack('heavy'))
        self.ui.Potion_button.clicked.connect(self.game.use_potion)
        self.ui.next_button.clicked.connect(self.game.handle_next)

    def pick_weapon(self, name):
        '''Allows user to select 2 weapons and begin the game. After these buttons are invisible'''
        if name not in self.selected_weapons:
            self.selected_weapons.append(name)

            all_weapon_choice_buttons = {
                'Axe': self.ui.Axe_button,
                'Sword': self.ui.Sword_button,
                'Spear': self.ui.Spear_button,
                'Dagger': self.ui.Dagger_button
            }

            all_weapon_choice_buttons[name].hide()

        if len(self.selected_weapons) == 2:
            self.ui.Begin_button.setEnabled(True)
            self.ui.text_label.setText('Press begin to start your mighty quest!')

    def begin_game(self):
        '''Starts game after initial weapon selection'''
        if len(self.selected_weapons) == 2:
            self.game.set_weapons(self.selected_weapons[0], self.selected_weapons[1])
            self.selected_weapons = []

def main():
    '''runs program'''
    app = QApplication(sys.argv)
    window = GameApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
