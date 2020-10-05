from Models.Components import (KILLABLE, MOVABLE, RENDERABLE, Component,
                               Killable, Movable, Renderable)
import uuid
from .goals import MOTH_GOALS
from .actions import MOTH_ACTIONS
from copy import deepcopy
from .forces import MOTH_FORCES
from SwinModules import Vector2D
from math import sin, cos, radians
from random import random, randrange, uniform


class Moth(object):
    def __init__(self, world, x=None, y=None):
        self.id = str(uuid.uuid4())
        self.type = "moth"
        self.world = world
        self.goals = deepcopy(MOTH_GOALS)
        self.current_action = MOTH_ACTIONS[0]
        self.discontentment = 60
        self.time_passed = 0
        self.goal_cooldown = 1.0
        if x is not None and y is not None:
            self.pos = Vector2D(x, y)
        else:
            self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        dir = radians(random()*360)
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()

        # Components
        self.components = {
            KILLABLE: Killable(),
            MOVABLE: Movable(parent=self, world=self.world, forces=MOTH_FORCES),
            RENDERABLE: Renderable(parent=self, color='GREEN')
        }
