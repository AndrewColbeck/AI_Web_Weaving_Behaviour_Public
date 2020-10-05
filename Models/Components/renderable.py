from .component import Component
from SwinModules import egi, Vector2D, Point2D
from math import sin, cos, radians
from random import random, randrange, uniform


RENDERABLE = 'Renderable'


class Renderable(Component):
    def __init__(self,  parent=None, color=None, stroke_size=2.0, scale=10.0):
        self.type = RENDERABLE
        self.parent = parent
        self.world = parent.world
        self.color = color
        self.stroke_size = stroke_size
        self.scale = Vector2D(scale, scale)
        self.shape = [
            Point2D(-1.0,  0.6),
            Point2D(1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]

    def update(self, delta):

        #  Draw Self
        egi.set_stroke(self.stroke_size)
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(
            self.shape, self.parent.pos, self.parent.heading, self.parent.side, self.scale)
        egi.closed_shape(pts)

        # Draw Influence Map
        if self.parent.type is "spider":
            for node in self.parent.prey_spottings:
                egi.set_pen_color(color=(1.0, 0.7, 0.7, node.hits))
                egi.rect(node.pos.x-20, node.pos.y+20,
                         node.pos.x+20, node.pos.y-20, filled=True)

            # Draw line of sight circle
            egi.set_pen_color(name='GREEN')
            egi.circle(self.parent.pos, self.parent.line_of_sight, slices=32)
