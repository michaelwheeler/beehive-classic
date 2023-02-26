import random

import pyxel

import input
from constants import LANES, SCREEN_HEIGHT, SCREEN_WIDTH
from entities import Garden, Hive


def get_random_lane():
    return random.randint(1, 7)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Beehive Classic", fps=60)
        pyxel.load("assets.pyxres")
        self.hive = Hive()
        self.garden = Garden()
        pyxel.run(self.update, self.draw)

    def update(self):
        if input.quit():
            pyxel.quit()
        self.garden.update()
        self.hive.update()
        for bee in self.hive.residents:
            for flower in self.garden.flowers:
                if bee.collision_space & flower.collision_space:
                    bee.recall()
                    flower.collect()

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
        self.garden.draw()
        self.hive.draw()


App()
