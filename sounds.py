from typing import NamedTuple

import pyxel

BEE_LAUNCH_IDX = 0
FLOWER_SPROUT_IDX = 1
FLOWER_WILT_IDX = 2
SPIDER_DEATH_IDX = 3
SPIDER_ATTACK_IDX = 4


class Sound(NamedTuple):
    notes: str
    tones: str
    volumes: str
    effects: str
    speed: int


placeholder_sfx = Sound("B3 B2", "ss", "55", "sf", 5)
bee_launch = Sound("e2 f1 e1 e1 e1", "p", "54321", "ssssf", 10)
flower_sprout = Sound("c1 e2 g3 c4", "t", "2345", "f", 5)
flower_wilt = Sound("c4 g3 e2 c1", "t", "2345", "f", 5)
spider_death = placeholder_sfx
spider_attack = placeholder_sfx


def init():
    pyxel.sounds[BEE_LAUNCH_IDX].set(*bee_launch)
    pyxel.sounds[FLOWER_SPROUT_IDX].set(*flower_sprout)
    pyxel.sounds[FLOWER_WILT_IDX].set(*flower_wilt)
    pyxel.sounds[SPIDER_DEATH_IDX].set(*spider_death)
    pyxel.sounds[SPIDER_ATTACK_IDX].set(*spider_attack)


def play_bee_launch():
    pyxel.play(0, BEE_LAUNCH_IDX)


def play_flower_sprout():
    pyxel.play(1, FLOWER_SPROUT_IDX)


def play_flower_wilt():
    pyxel.play(1, FLOWER_WILT_IDX)


def play_spider_death():
    pyxel.play(0, SPIDER_DEATH_IDX)


def play_spider_attack():
    pyxel.play(0, SPIDER_ATTACK_IDX)
