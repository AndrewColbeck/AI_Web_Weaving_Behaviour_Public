import random
from random import randrange
from pyglet import clock
from Controllers import ObjectPoolController, UserInputController
from Models import World
from Views import UIView

config = {
    "world size": (800, 800),
    "number of spiders": 1,
    "number of moths": 5,
    "verbose": False
}

if __name__ == '__main__':
    # create a world for agents
    world = World(config)

    # # initialise controllers
    object_pool_controller = ObjectPoolController(world)
    user_input_controller = UserInputController(world, object_pool_controller)
    ui = UIView(world, user_input_controller, object_pool_controller)

    # # add agents
    for i in range(0, config["number of spiders"]):
        object_pool_controller.add_agent(
            type='spider', x=50, y=50)

    def update(self):
        ui.update()

    while not ui.win.has_exit:
        # processInput
        user_input_controller.on_key_held()

        # update
        delta = clock.tick()
        ui.update()
        world.update(delta)
        object_pool_controller.update(delta)

        # render
        ui.render(delta)
