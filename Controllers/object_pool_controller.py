# from random import randrange
# from .prey import Prey
# from .hunter import Hunter
# from .world import World
# from .Libraries.vector2d import Vector2D
from .spider_controller import SpiderController
from .moth_controller import MothController
from .web_controller import WebController


class ObjectPoolController(object):
    def __init__(self, world):
        self.world = world
        self.moth_controller = MothController(world)
        self.spider_controller = SpiderController(
            world)
        self.web_controller = WebController(world)

    def add_agent(self, type, x=None, y=None):
        if type == "spider":
            new_web = self.spider_controller.add_agent(
                x, y)
            self.web_controller.add_web(new_web)
        if type == "moth":
            self.moth_controller.add_agent(x, y)

    def update(self, delta):
        self.spider_controller.update(delta)
        self.moth_controller.update(delta)
        self.web_controller.update(delta, self.spider_controller.spiders)

    def render(self, delta):
        self.spider_controller.render(delta)
        self.moth_controller.render(delta)
        self.web_controller.render()

    def add_prey_spotted(self, x, y):
        self.spider_controller.add_prey_spotted(x, y)
