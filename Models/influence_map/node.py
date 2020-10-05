from SwinModules import Vector2D


class Node(object):
    def __init__(self, pos):
        self.pos = pos
        self.hits = 1.0

    def increment_hits(self):
        if self.hits < 1:
            self.hits += 0.1

    def decrement_hits(self):
        if self.hits > 0:
            self.hits -= 0.001
