import random
from enum import Enum, auto
from typing import List, NamedTuple, Optional, Tuple

import pyxel

import input
from constants import LANES, SCREEN_HEIGHT


class Sprite(NamedTuple):
    img: int
    u: int
    v: int
    w: int
    h: int
    colkey: int


class BeeStatus(Enum):
    READY = 0
    OUTBOUND = 1
    INBOUND = -1


class Bee:
    lane: int = 4
    frame_created: int = 0
    frame_launched: int = 0
    frame_recalled: int = 0

    def __init__(self, slot: int) -> None:
        self.lane = slot
        self.frame_created = pyxel.frame_count

    def launch(self) -> None:
        self.frame_launched = pyxel.frame_count

    def recall(self) -> None:
        self.frame_recalled = pyxel.frame_count

    def inc_lane(self) -> None:
        if self.lane == 7:
            self.lane = 1
        else:
            self.lane += 1

    def dec_lane(self) -> None:
        if self.lane == 1:
            self.lane = 7
        else:
            self.lane -= 1

    @property
    def status(self) -> BeeStatus:
        if self.frame_recalled:
            return BeeStatus.INBOUND
        if self.frame_launched:
            return BeeStatus.OUTBOUND
        return BeeStatus.READY

    @property
    def x(self) -> int:
        return LANES[self.lane - 1] + 4

    @property
    def y(self) -> int:
        screen_bottom = SCREEN_HEIGHT - 8
        if self.status == BeeStatus.READY:
            return screen_bottom
        if self.status == BeeStatus.OUTBOUND:
            frames_since_launch = pyxel.frame_count - self.frame_launched
            y_pos = screen_bottom - (2 * frames_since_launch)
            if y_pos <= 0:
                self.recall()
            else:
                return y_pos
        if self.status == BeeStatus.INBOUND:
            screen_top = 0
            frames_since_recall = pyxel.frame_count - self.frame_recalled
            return screen_top + (2 * frames_since_recall)

    @property
    def sprite(self) -> Tuple[int, int]:
        bee_sprites = [
            (0, 0),
            (8, 0),
            (0, 8),
            (8, 8),
        ]
        idx = (pyxel.frame_count // 2) % 4
        return bee_sprites[idx]

    @property
    def departed(self) -> bool:
        return self.y > 128

    def draw(self):
        x = self.x
        y = self.y
        img = 0
        u, v = self.sprite
        w = 8
        h = -8 if self.status == BeeStatus.INBOUND else 8
        pyxel.blt(x, y, img, u, v, w, h)


class Hive:
    residents: List[Bee] = []
    lane: int = 4
    capacity: int = 3

    def __init__(self):
        self.residents.append(Bee(self.lane))

    def inc_lane(self) -> None:
        if self.lane == 7:
            self.lane = 1
        else:
            self.lane += 1
        if self.ready_bee is not None:
            self.ready_bee.lane = self.lane

    def dec_lane(self) -> None:
        if self.lane == 1:
            self.lane = 7
        else:
            self.lane -= 1
        if self.ready_bee is not None:
            self.ready_bee.lane = self.lane

    def launch(self) -> None:
        if self.ready_bee is not None:
            self.ready_bee.launch()

    @property
    def remaining(self) -> List[Bee]:
        return [bee for bee in self.residents if not bee.departed]

    @property
    def has_bee_ready(self) -> bool:
        return BeeStatus.READY in [bee.status for bee in self.residents]

    @property
    def ready_bee(self) -> Optional[Bee]:
        ready_bees = [bee for bee in self.residents if bee.status == BeeStatus.READY]
        return ready_bees[0] if ready_bees else None

    @property
    def has_vacancy(self):
        return self.capacity > len(self.residents)

    def update(self):
        self.residents = self.remaining
        if self.has_vacancy and self.ready_bee is None:
            self.residents.append(Bee(self.lane))
        if input.launch():
            self.launch()
        if input.right():
            self.inc_lane()
        if input.left():
            self.dec_lane()

    def draw_ghost_bee(self):
        pyxel.blt(
            x=LANES[self.lane - 1] + 4,
            y=120 - 8,
            img=0,
            u=0,
            v=16,
            w=8,
            h=8,
            colkey=pyxel.COLOR_LIME,
        )

    def draw(self):
        for bee in self.residents:
            bee.draw()
        if self.ready_bee is None:
            self.draw_ghost_bee()


class FlowerStatus(Enum):
    GROWING = auto()
    BLOOMING = auto()
    WILTING = auto()
    GONE = auto()


class Flower:
    lane: int = 4
    position: int = 0
    growth_duration: int = 20
    frame_sprouted: int = 0
    frame_collected: int = 0

    def __init__(self, lane: int, position: int, growth_duration: int = 20) -> None:
        self.lane = lane
        self.position = position
        self.growth_duration = growth_duration
        self.frame_sprouted = pyxel.frame_count

    @property
    def frame_blooms(self) -> int:
        return self.frame_sprouted + self.growth_duration

    @property
    def status(self) -> FlowerStatus:
        if pyxel.frame_count < self.frame_blooms:
            return FlowerStatus.GROWING
        if not self.frame_collected:
            return FlowerStatus.BLOOMING
        if pyxel.frame_count < self.frame_collected + 30:
            return FlowerStatus.WILTING
        return FlowerStatus.GONE

    @property
    def x(self) -> int:
        return (self.lane - 1) * 22 + 6

    @property
    def y(self) -> int:
        return self.position

    @property
    def sprite(self) -> Sprite:
        u = 32
        v = 0
        return Sprite(0, u, v, 16, 16, pyxel.COLOR_LIME)

    def collect(self):
        if self.status != FlowerStatus.WILTING:
            self.frame_collected = pyxel.frame_count

    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite)


class Garden:
    MAX_HEIGHT = 100
    MIN_HEIGHT = 40
    MAX_FLOWERS = 3
    flowers: List[Flower] = []

    def plant_flower(self):
        if len(self.flowers) < self.MAX_FLOWERS:
            column = random.randint(1, 7)
            height = random.randint(self.MIN_HEIGHT, self.MAX_HEIGHT)
            self.flowers.append(Flower(column, height))

    @property
    def is_empty(self) -> bool:
        return bool(self.flowers)

    @property
    def frames_since_last_planted(self) -> int:
        if not self.flowers:
            return pyxel.frame_count
        frame_last_planted = max([flower.frame_sprouted for flower in self.flowers])
        return pyxel.frame_count - frame_last_planted

    def update(self):
        self.flowers = [
            flower for flower in self.flowers if flower.status != FlowerStatus.GONE
        ]
        if self.frames_since_last_planted > 120:
            self.plant_flower()

    def draw(self):
        for flower in self.flowers:
            flower.draw()
