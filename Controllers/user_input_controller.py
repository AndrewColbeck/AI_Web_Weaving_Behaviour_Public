# from .world import World
# from .Libraries.graphics import KEY
from Models import World
from SwinModules import KEY


class UserInputController(object):

    def __init__(self, world=None, object_pool=None):
        # keep a reference to the world object
        self.world = world
        # object pool handled crud operations for agents
        self.object_pool = object_pool
        # Holding Keys down
        self.keyboard = KEY.KeyStateHandler()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:  # left
            self.object_pool.add_prey_spotted(x, y)

    def on_key_press(self, symbol, modifiers):
        if symbol == KEY.A:
            for i in range(0, self.world.config["number of moths"]):
                self.object_pool.add_agent(type='moth')

        elif symbol == KEY.C:
            self.world.moths.clear()

        # Toggle debug force line info on the agent
        elif symbol == KEY.I:
            for agent in self.world.agents:
                agent.show_info = not agent.show_info

        elif symbol == KEY.P:
            self.world.paused = not self.world.paused

        # elif symbol == KEY.U:
        #     self.object_pool.update(delta)

    def on_key_held(self):
        if self.keyboard[KEY.MINUS]:
            print("KEY PRESSED: MINUS KEY")
        if self.keyboard[KEY.EQUAL]:
            print("KEY PRESSED: PLUS KEY")
