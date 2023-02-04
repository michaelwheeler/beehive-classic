import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Beehive Classic")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, "Beehive Classic", pyxel.COLOR_YELLOW)


App()
