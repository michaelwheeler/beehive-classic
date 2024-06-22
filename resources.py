from enum import Enum, auto

import pyxel

import events
import input
import sounds
import text
from constants import SCREEN_WIDTH


class GameMode(Enum):
    TITLE_SCREEN = auto()
    PLAYING = auto()
    GAME_OVER = auto()


class Game:
    mode = GameMode.TITLE_SCREEN
    lives = 3
    score: int = 0

    @property
    def is_active(self):
        return self.mode is GameMode.PLAYING

    def start_game(self):
        self.score = 0
        self.lives = 3
        self.mode = GameMode.PLAYING

    def end_game(self):
        self.mode = GameMode.GAME_OVER
        events.game_over()

    def increment_score(self, amount: int = 1):
        self.score += amount

    def reduce_lives(self, amount: int = 1):
        if self.lives > 1:
            self.lives -= amount
        else:
            self.lives = 0
            self.end_game()

    def handle_spider_attack(self, spider):
        self.reduce_lives()
        sounds.play_spider_attack()

    def update(self):
        if self.mode in (GameMode.TITLE_SCREEN, GameMode.GAME_OVER):
            if input.start():
                self.start_game()

    def draw_life(self, num):
        width = 2
        height = 3
        color = pyxel.COLOR_GREEN if self.lives < num else pyxel.COLOR_WHITE
        x = SCREEN_WIDTH - 25 + num * 6
        y = 4
        pyxel.rect(x, y, width, height, color)
        pyxel.pset(x - 1, y + 1, color)
        pyxel.pset(x + width, y + 1, color)

    def draw(self):
        if self.mode == GameMode.TITLE_SCREEN:
            text.centered("Beehive Classic", y=50, color=pyxel.COLOR_WHITE)
            text.centered("Press SPACE to start", y=60, color=pyxel.COLOR_GREEN)
        if self.mode in (GameMode.PLAYING, GameMode.GAME_OVER):
            text.left(f"Score: {self.score}", y=text.TOP)
            text.centered("Beehive Classic", y=text.TOP, color=pyxel.COLOR_GREEN)
            for life in range(1, 4):
                self.draw_life(life)
        if self.mode == GameMode.GAME_OVER:
            text.centered("GAME OVER")
            text.centered("Press SPACE to play again", y=60, color=pyxel.COLOR_GREEN)
