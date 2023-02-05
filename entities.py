from enum import Enum
from typing import Tuple

import pyxel

from constants import LANES, SCREEN_HEIGHT


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
