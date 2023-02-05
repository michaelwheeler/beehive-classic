import pyxel

from constants import LANES, SCREEN_HEIGHT, SCREEN_WIDTH
from entities import Bee, BeeStatus


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Beehive Classic", fps=60)
        pyxel.load("assets.pyxres")
        self.bees = [Bee(4)]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.bees = [bee for bee in self.bees if not bee.departed]
        if not len(self.bees):
            self.bees.append(Bee(4))
        if pyxel.btnp(pyxel.KEY_SPACE):
            for bee in self.bees:
                if bee.status == BeeStatus.READY:
                    bee.launch()
        if pyxel.btnp(pyxel.KEY_RIGHT):
            for bee in self.bees:
                if bee.status == BeeStatus.READY:
                    bee.inc_lane()
        if pyxel.btnp(pyxel.KEY_LEFT):
            for bee in self.bees:
                if bee.status == BeeStatus.READY:
                    bee.dec_lane()

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
        for bee in self.bees:
            bee.draw()


App()
