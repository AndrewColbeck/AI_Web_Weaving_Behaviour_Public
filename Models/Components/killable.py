from .component import Component

KILLABLE = 'Killable'


class Killable(Component):
    def __init__(self):
        self.type = KILLABLE

    def update(self, delta):
        pass
