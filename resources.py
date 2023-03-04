import pyxel


class Game:
    score: int = 0

    def increment_score(self, amount: int = 1):
        self.score += amount

    def draw(self):
        pyxel.text(96, 3, "Beehive Classic", pyxel.COLOR_GREEN)
        pyxel.text(6, 3, f"Score: {self.score}", pyxel.COLOR_WHITE)
