import pyxel


def quit():
    return pyxel.btnp(pyxel.KEY_Q)


def start():
    return any(
        (
            pyxel.btnp(pyxel.KEY_SPACE),
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A),
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B),
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X),
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y),
        )
    )


def launch():
    return pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)


def right():
    return pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)


def left():
    return pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
