import random

import pyxel

import events
import input
from constants import LANES, SCREEN_HEIGHT, SCREEN_WIDTH
from entities import Garden, Hive
from resources import Game


def get_random_lane():
    return random.randint(1, 7)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Beehive Classic", fps=60)
        pyxel.load("assets.pyxres")
        pyxel.image(1).load(0, 0, "flower.png")
        self.game = Game()
        self.hive = Hive()
        self.garden = Garden()
        events.spider_attack.append(self.game.handle_spider_attack)
        events.game_over.append(self.garden.handle_game_over)
        events.game_over.append(self.hive.handle_game_over)
        pyxel.run(self.update, self.draw)

    def update(self):
        if input.quit():
            pyxel.quit()
        if self.game.is_active:
            self.garden.update()
            self.hive.update()
            spiders = [spider for spider in self.garden.spiders if spider.y < 100]
            for bee in self.hive.residents:
                for flower in self.garden.blooming_flowers:
                    if bee.collision_space & flower.collision_space:
                        self.game.increment_score()
                        bee.recall()
                        flower.collect()
                for spider in spiders:
                    if bee.collision_space & spider.collision_space:
                        spider.destroy()
                        bee.recall()
        self.game.update()

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
        self.game.draw()
        if self.game.is_active:
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
