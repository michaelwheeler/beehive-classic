class Event(list):
    def __call__(self, *args, **kwargs):
        for receiver in self:
            receiver(*args, **kwargs)


spider_attack = Event()

game_over = Event()
