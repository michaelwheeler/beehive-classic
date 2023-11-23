import random
from enum import Enum, auto
from typing import List, NamedTuple, Optional, Set

import pyxel

import events
import input
from constants import LANES, SCREEN_HEIGHT


class Sprite(NamedTuple):
    img: int
    u: int
    v: int
    w: int
    h: int
    colkey: int


class Location(NamedTuple):
    x: int
    y: int


class Coordinates(NamedTuple):
    row: int
    column: int


def pixelbox(x: int, y: int, w: int, h: int) -> Set[Location]:
    return set(Location(x1, y1) for x1 in range(x, x + w) for y1 in range(y, y + h))


def draw_pixels(pixels: Set[Location], color: int = pyxel.COLOR_RED):
    for pixel in pixels:
        pyxel.rect(pixel.x, pixel.y, 1, 1, color)


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
        if self.status is not BeeStatus.INBOUND:
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
        match self.status:
            case BeeStatus.READY:
                return screen_bottom
            case BeeStatus.OUTBOUND:
                frames_since_launch = pyxel.frame_count - self.frame_launched
                y_pos = screen_bottom - (2 * frames_since_launch)
                if y_pos <= 0:
                    self.recall()
                return y_pos
            case BeeStatus.INBOUND:
                frames_since_launch = self.frame_recalled - self.frame_launched
                y_pos = screen_bottom - (2 * frames_since_launch)
                frames_since_recall = pyxel.frame_count - self.frame_recalled
                return y_pos + (2 * frames_since_recall)

    @property
    def collision_space(self) -> Set[Location]:
        return pixelbox(self.x + 2, self.y + 1, 4, 6)

    @property
    def sprite(self) -> Sprite:
        bee_sprites = [
            (0, 0),
            (8, 0),
            (0, 8),
            (8, 8),
        ]
        idx = (pyxel.frame_count // 2) % 4
        u, v = bee_sprites[idx]
        return Sprite(
            0, u, v, 8, -8 if self.status is BeeStatus.INBOUND else 8, pyxel.COLOR_LIME
        )

    @property
    def departed(self) -> bool:
        return self.y > 128

    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite)


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

    def handle_game_over(self):
        self.residents = []
        self.lane = 4
        self.residents.append(Bee(self.lane))

    @property
    def remaining(self) -> List[Bee]:
        return [bee for bee in self.residents if not bee.departed]

    @property
    def has_bee_ready(self) -> bool:
        return BeeStatus.READY in [bee.status for bee in self.residents]

    @property
    def ready_bee(self) -> Optional[Bee]:
        ready_bees = [bee for bee in self.residents if bee.status is BeeStatus.READY]
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
    row: int = 0
    lane: int = 4
    flip: bool = False
    growth_duration: int = 24
    frame_sprouted: int = 0
    frame_collected: int = 0

    def __init__(self, lane: int, row: int, growth_duration: int = 20) -> None:
        self.lane = lane
        self.row = row
        self.flip = bool(pyxel.rndi(0, 1))
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
    def coordinates(self) -> Coordinates:
        return Coordinates(self.row, self.lane)

    @property
    def x(self) -> int:
        return (self.lane - 1) * 22 + 6

    @property
    def y(self) -> int:
        return self.row * 20

    @property
    def collision_space(self) -> Set[Location]:
        return pixelbox(self.x + 5, self.y + 1, 6, 5)

    @property
    def sprite(self) -> Sprite:
        match self.status:
            case FlowerStatus.GROWING:
                frames_since_sprout = pyxel.frame_count - self.frame_sprouted
                u = 16 * int(frames_since_sprout / 4)
            case FlowerStatus.WILTING:
                frames_since_collection = pyxel.frame_count - self.frame_collected
                u = 80 - 16 * int(frames_since_collection / 4)
            case _:
                u = 80
        v = 0
        w = -16 if self.flip else 16
        return Sprite(1, u, v, w, 16, pyxel.COLOR_LIME)

    def collect(self):
        if self.status is not FlowerStatus.WILTING:
            self.frame_collected = pyxel.frame_count

    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite)


class SpiderStatus(Enum):
    CRAWLING = auto()
    DYING = auto()
    GONE = auto()
    ATTACKING = auto()


class Spider:
    lane: int = 4
    frame_created: int = 0
    frame_destroyed: int = 0
    speed: int = 1

    def __init__(self, lane: int, speed: int = 1) -> None:
        self.lane = lane
        self.frame_created = pyxel.frame_count

    @property
    def status(self) -> SpiderStatus:
        if self.frame_destroyed == 0:
            start = -16
            frames_alive = pyxel.frame_count - self.frame_created
            y_pos = start + frames_alive * self.speed
            return SpiderStatus.CRAWLING if y_pos < 100 else SpiderStatus.ATTACKING
        if pyxel.frame_count - self.frame_destroyed > 11:
            return SpiderStatus.GONE
        return SpiderStatus.DYING

    @property
    def x(self) -> int:
        return (self.lane - 1) * 22 + 6

    @property
    def y(self) -> int:
        max_frame = (
            pyxel.frame_count
            if self.status is SpiderStatus.CRAWLING
            else self.frame_destroyed
        )
        start = -16
        frames_alive = max_frame - self.frame_created
        return start + frames_alive * self.speed

    @property
    def collision_space(self) -> Set[Location]:
        return pixelbox(self.x + 5, self.y + 5, 6, 6)

    @property
    def sprite(self) -> Sprite:
        u = 16
        v = 0
        if self.status is SpiderStatus.DYING:
            v = 16 * (pyxel.frame_count - self.frame_destroyed)
        return Sprite(0, u, v, 16, 16, pyxel.COLOR_LIME)

    def destroy(self):
        self.frame_destroyed = pyxel.frame_count

    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite)


class Garden:
    MAX_ROW = 4
    MIN_ROW = 1
    MAX_FLOWERS = 3
    flowers: List[Flower] = []
    spiders: List[Spider] = []

    def plant_flower(self):
        if len(self.flowers) < self.MAX_FLOWERS:
            column = random.randint(1, 7)
            row = random.randint(self.MIN_ROW, self.MAX_ROW)
            if (row, column) not in [flower.coordinates for flower in self.flowers]:
                self.flowers.append(Flower(column, row))

    def launch_spider(self):
        column = random.randint(1, 7)
        self.spiders.append(Spider(lane=column))

    @property
    def is_empty(self) -> bool:
        return bool(self.flowers)

    @property
    def frames_since_last_planted(self) -> int:
        if not self.flowers:
            return pyxel.frame_count
        frame_last_planted = max([flower.frame_sprouted for flower in self.flowers])
        return pyxel.frame_count - frame_last_planted

    @property
    def frames_since_last_spider(self) -> int:
        if not self.spiders:
            return pyxel.frame_count
        last_spider_launch = max([spider.frame_created for spider in self.spiders])
        return pyxel.frame_count - last_spider_launch

    @property
    def blooming_flowers(self):
        return [
            flower for flower in self.flowers if flower.status == FlowerStatus.BLOOMING
        ]

    def handle_game_over(self):
        self.flowers = []
        self.spiders = []

    def update(self):
        self.flowers = [
            flower for flower in self.flowers if flower.status != FlowerStatus.GONE
        ]
        attacking_spiders = [
            spider for spider in self.spiders if spider.status == SpiderStatus.ATTACKING
        ]
        self.spiders = [
            spider
            for spider in self.spiders
            if spider.status not in (SpiderStatus.GONE, SpiderStatus.ATTACKING)
        ]
        if self.frames_since_last_planted > 120:
            self.plant_flower()
        if self.frames_since_last_spider > 200:
            self.launch_spider()
        for spider in attacking_spiders:
            events.spider_attack(spider)

    def draw(self):
        for flower in self.flowers:
            flower.draw()
        for spider in self.spiders:
            spider.draw()
