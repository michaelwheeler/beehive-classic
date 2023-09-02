import pyxel

from constants import SCREEN_WIDTH

TOP = 3


def text_width(text: str) -> int:
    return max(len(text) * 4 - 1, 0)


def centered(text, y=50, color=pyxel.COLOR_WHITE):
    pyxel.text(
        (SCREEN_WIDTH - text_width(text)) / 2,
        y,
        text,
        color,
    )


def left(text, y=50, color=pyxel.COLOR_WHITE):
    pyxel.text(
        4,
        y,
        text,
        color,
    )


def right(text, y=50, color=pyxel.COLOR_WHITE):
    pyxel.text(
        SCREEN_WIDTH - 4 - text_width(text),
        y,
        text,
        color,
    )
