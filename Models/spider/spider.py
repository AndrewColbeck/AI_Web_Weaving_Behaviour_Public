from Models.Components import (KILLABLE, MOVABLE, RENDERABLE, Component,
                               Killable, Movable, Renderable)
import uuid
from .goals import SPIDER_GOALS
from .actions import SPIDER_ACTIONS
from copy import deepcopy
from .forces import SPIDER_FORCES
from SwinModules import Vector2D
from math import sin, cos, radians
from random import random, randrange, uniform
from Models.influence_map import Node
from SwinModules import Path
from Models.web import Web


class Spider(object):
    def __init__(self, world, x=None, y=None):
        self.id = str(uuid.uuid4())
        self.type = "spider"
        self.world = world
        self.goals = deepcopy(SPIDER_GOALS)
        self.current_action = SPIDER_ACTIONS[0]
        self.discontentment = 60
        self.time_passed = 0
        self.web_planning_time_passed = 0
        self.moth_last_spotted = 0
        self.goal_cooldown = 1.0
        self.web_planning_cooldown = 0.01
        self.moth_spotting_cooldown = 0.01
        self.line_of_sight = 200
        self.prey_spottings = []
        self.web = Web()

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
            MOVABLE: Movable(parent=self, world=self.world, forces=SPIDER_FORCES),
            RENDERABLE: Renderable(parent=self, color='RED')
        }
