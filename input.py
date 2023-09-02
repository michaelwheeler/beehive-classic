import pyxel


def quit():
    return pyxel.btnp(pyxel.KEY_Q)


def start():
    return pyxel.btnp(pyxel.KEY_SPACE)


def launch():
    return pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)


def right():
    return pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)


def left():
    return pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
