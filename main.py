import pyxel

from constants import LANES, SCREEN_HEIGHT, SCREEN_WIDTH
from entities import Hive


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Beehive Classic", fps=60)
        pyxel.load("assets.pyxres")
        self.hive = Hive()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.hive.update()

    def draw_exit(self, x):
        height = 5
        pyxel.rect(
            x,
            y=SCREEN_HEIGHT - height,
            w=16,
            h=height,
            col=pyxel.COLOR_LIME,
        )

    def draw(self):
        pyxel.cls(pyxel.COLOR_LIME)
        pyxel.text(55, 41, "Beehive Classic", pyxel.COLOR_GREEN)
        pyxel.rect(
            x=0,
            y=115,
            w=SCREEN_WIDTH,
            h=5,
            col=pyxel.COLOR_NAVY,
        )
        for lane in LANES:
            self.draw_exit(lane)
        self.hive.draw()


App()
