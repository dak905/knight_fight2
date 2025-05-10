import random
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap

class Game:
    def __init__(self, window):
        '''starts game with the PYQT6 window'''
        self.window = window
        self.reset_game()

#reset stats to starting values
    def reset_game(self):
        '''Starts a fresh run of the game with starting values after reset'''
        self.player_health = 100
        self.orc_health = 50
        self.dragon_health = 120
        self.potions = 2
        self.weapons = []
        self.turn_ready = False
        self.combat_stage = 'picking_gear'
        self.show_start_ui()


#starting attributes (health, full potions, starting text, healthy knight, also prevents attacking)
    def show_start_ui(self):
        '''Sets all values necessary for a new game, and prevents attacking or using potions'''
        self.window.text_label.setText('Welcome Adventurer! Please select two weapons to begin your journey!')
        self.window.Light_button.hide()
        self.window.Heavy_button.hide()
        self.window.Potion_button.hide()
        self.window.next_button.hide()
        self.window.Potion_button.setText('Potion 2/2')
        self.window.health_label.setText('100/100')

        self.set_scaled_sprite(self.window.player_picture, 'gui/sprites/healthy_knight.png')
        self.window.enemy_picture.clear()

        self.window.Axe_button.show()
        self.window.Sword_button.show()
        self.window.Spear_button.show()
        self.window.Dagger_button.show()
        self.window.Begin_button.show()
        self.window.Begin_button.setEnabled(False)

#fix picking weapons and not being able to attack without starting the game
    def set_weapons(self, weapon_one, weapon_two):
        '''gives player weapons connected to heavy and light attacks and puts you into combat with the orc'''
        self.weapons = [weapon_one, weapon_two]
        self.window.text_label.setText('You encounter an orc! Ready your arms!')

        self.window.Axe_button.hide()
        self.window.Sword_button.hide()
        self.window.Spear_button.hide()
        self.window.Dagger_button.hide()
        self.window.Begin_button.hide()

        self.window.Light_button.show()
        self.window.Heavy_button.show()
        self.window.Potion_button.show()
        self.window.next_button.hide()

        self.combat_stage = 'orc'
        self.turn_ready = True
        self.update_enemy_sprite()
        self.let_attack(True)

#weapon damage dice for all weapons
    def roll_damage(self, weapon):
        '''Rolls damage for all weapons'''
        if weapon == 'Axe':
            return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6) + 4
        if weapon == 'Sword':
            return random.randint(1, 6) + random.randint(1, 6) + 4
        if weapon == 'Spear':
            return random.randint(1, 8) + random.randint(1, 8) + 4
        if weapon == 'Dagger':
            return random.randint(1, 6) + 4
        return 0

# I initially had all the turns seperated between player and enemy turns all controlled by the next_button, but that ended up giving me too many errors so I switched to them all happening at the same time. Because of this I needed something to cycle from player to enemy combat sentences in the same turn. To do this I found documentation about Qtimer which I had never used before. h
# documentation I used https://doc.qt.io/qtforpython-5/PySide2/QtCore/QTimer.html
# https://stackoverflow.com/questions/23860665/using-qtimer-singleshot-correctly




    # assign weapons to heavy or light, also player combat sentence
    def player_attack(self, kind):
        '''sets weapons to light or heavy, gets damage from roll_damage and updates the combat sentence'''
        if not self.turn_ready:
            return

        weapon_one = self.weapons[0]
        weapon_two = self.weapons[1]

        damage_one = self.roll_damage(weapon_one)
        damage_two = self.roll_damage(weapon_two)

        if damage_one > damage_two:
            hvy = weapon_one
            lgt = weapon_two
        else:
            hvy = weapon_two
            lgt = weapon_one

        if kind == 'heavy':
            weapon = hvy
            hit = random.random() <= 0.658
        else:
            weapon = lgt
            hit = random.random() <= 0.875

        damage = self.roll_damage(weapon) if hit else 0

        if self.combat_stage == 'orc':
            self.orc_health -= damage
            target = 'orc'
        else:
            self.dragon_health -= damage
            target = 'dragon'

        self.window.text_label.setText(f'You {"hit" if hit else "missed"} the {target} dealing {damage} damage!')
        self.update_enemy_sprite()

        self.turn_ready = False
        self.let_attack(False)
        QTimer.singleShot(1500, self.enemy_turn)

    #potion stuff
    def use_potion(self):
        '''heals player, lowers potion count after use and gives text when no potions are left'''
        if not self.turn_ready:
            return
        if self.potions > 0:
            self.player_health += 25
            if self.player_health > 100:
                self.player_health = 100
            self.potions -= 1
            self.window.Potion_button.setText(f'Potion {self.potions}/2')
            self.window.text_label.setText('You used a potion and healed 25 health!')
        else:
            self.window.text_label.setText('Out of potions try an attack')

        self.window.health_label.setText(f'{self.player_health}/100')
        self.update_knight_sprite()

        self.turn_ready = False
        self.let_attack(False)
        QTimer.singleShot(1500, self.enemy_turn)

#enemy hit "roll" and dmg, and combat sentence for both orc, and dragon
    def enemy_turn(self):
        '''Runs enemy attacks, returns combat sentence, updates player health (when damaged) and deals with death sentences'''
        if self.combat_stage == 'orc':
            hit = random.random() < 0.70
            damage = random.randint(5, 12) if hit else 0
            monster = 'orc'
        else:
            hit = random.random() < 0.60
            damage = random.randint(10, 20) if hit else 0
            monster = 'dragon'

        self.player_health -= damage
        if self.player_health < 0:
            self.player_health = 0

        self.window.text_label.setText(f'The {monster} {"hits" if hit else "misses"} you for {damage} damage!')
        self.window.health_label.setText(f'{self.player_health}/100')
        self.update_knight_sprite()

        if self.player_health <= 0:
            self.retry(f'The {monster} has slain you!')
        elif self.combat_stage == 'orc' and self.orc_health <= 0:
            self.window.text_label.setText('You have vanquished the orc! Suddenly a dragon appears get ready!')
            self.combat_stage = 'dragon'
            self.turn_ready = True
            self.update_enemy_sprite()
            self.let_attack(True)
        elif self.combat_stage == 'dragon' and self.dragon_health <= 0:
            self.retry('You have slain the dragon! Victory is yours!')
        else:
            self.turn_ready = True
            self.let_attack(True)

#reset after die or win
    def retry(self, message):
        '''Reviles retry button and prevents the player from attacking'''
        self.window.text_label.setText(message)
        self.update_enemy_sprite()
        self.window.Light_button.hide()
        self.window.Heavy_button.hide()
        self.window.Potion_button.hide()
        self.window.next_button.setText('Retry')
        self.window.next_button.show()
        self.turn_ready = False
        self.combat_stage = 'end'

#show reset button
    def handle_next(self):
        '''Resets the game when the retry/next button is clicked'''
        if self.combat_stage == 'end':
            self.reset_game()

#prevent attacking when dead or at the begining
    def let_attack(self, enabled):
        '''Opens accesabilty to attack, and potion buttons when in combat, closes them when out of combat'''
        self.window.Light_button.setEnabled(enabled)
        self.window.Heavy_button.setEnabled(enabled)
        self.window.Potion_button.setEnabled(enabled)




#  This was my first time ever working with sprites so I had to look at videos to understand how it works. Also ran into a problem with the scaling initialy so I had to watch another video on that.
# images video: https://youtu.be/D0iCHFXHb_g?si=ejZdx4yPnzYiu7Lz
#scaling video: https://youtu.be/SlGp3zSWibE?si=zaGD3FnQcQrDAKG5
# other video I used https://www.youtube.com/watch?v=c_3gC_y0Aac
# documentation I used for pixmap https://doc.qt.io/qtforpython-5/PySide2/QtGui/QPixmap.html



# sprite changing when reaching 1/2 health then again when dead
    def update_knight_sprite(self):
        '''change portrait of knight based on state (healthy, hurt, dead)'''
        if self.player_health == 0:
            self.set_scaled_sprite(self.window.player_picture, 'gui/sprites/dead_knight.png')
        elif self.player_health <= 49:
            self.set_scaled_sprite(self.window.player_picture, 'gui/sprites/hurt_knight.png')
        else:
            self.set_scaled_sprite(self.window.player_picture, 'gui/sprites/healthy_knight.png')

    def update_enemy_sprite(self):
        '''change portrait of orc and dragon based on state (healthy, hurt, dead)'''
        if self.combat_stage == 'orc':
            if self.orc_health <= 0:
                self.set_scaled_sprite(self.window.enemy_picture, 'gui/sprites/dead_orc.png')
            elif self.orc_health <= 25:
                self.set_scaled_sprite(self.window.enemy_picture, 'gui/sprites/hurt_orc.png')
            else:
                self.set_scaled_sprite(self.window.enemy_picture, 'gui/sprites/healthy_orc.png')
        elif self.combat_stage == 'dragon':
            if self.dragon_health <= 0:
                self.set_scaled_sprite(self.window.enemy_picture, 'gui/sprites/dead_dragon.png')
            elif self.dragon_health <= 75:
                self.set_scaled_sprite(self.window.enemy_picture, 'gui/sprites/hurt_dragon.png')
            else:
                self.set_scaled_sprite(self.window.enemy_picture, 'gui/sprites/healthy_dragon.png')

#fix size of sprites
    def set_scaled_sprite(self, label, image_path):
        '''Created proper sizing for sprites to fill the whole label.'''
        pixmap = QPixmap(image_path)
        scaled = pixmap.scaled(label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        label.setPixmap(scaled)


