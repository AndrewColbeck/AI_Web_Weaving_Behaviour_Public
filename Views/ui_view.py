from pyglet import window, clock
from pyglet.gl import \
    glEnable, GL_BLEND, glBlendFunc, \
    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, \
    glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

from SwinModules import egi, KEY, COLOR_NAMES
from Controllers import UserInputController
# from .Libraries.graphics import egi, KEY, COLOR_NAMES
# from ..Controllers import UserInputController
# from .user_input_controller import UserInput
# from .graphics import egi, KEY, COLOR_NAMES


class UIView(object):
    def on_resize(self, cx, cy):
        self.world.cx = cx
        self.world.cy = cy

    def __init__(self, world=None, user_input_controller=None, object_pool_controller=None):
        self.world = world
        self.object_pool_controller = object_pool_controller
        # create a pyglet window and set glOptions
        self.win = window.Window(
            width=world.cy, height=world.cx, vsync=True, resizable=True)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # needed so that egi knows where to draw
        egi.InitWithPyglet(self.win)
        # prep the fps display
        self.fps_display = window.FPSDisplay(self.win)

        # User Input Stuff / register key and mouse event handlers
        self.user_input_controller = user_input_controller
        self.win.push_handlers(self.user_input_controller.on_key_press)
        self.win.push_handlers(self.user_input_controller.on_mouse_press)
        self.win.push_handlers(self.user_input_controller.keyboard)
        self.win.push_handlers(self.on_resize)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def update(self):
        self.win.dispatch_events()

    def render(self, delta):
        self.clear()
        self.world.render()

        self.object_pool_controller.render(delta)
        self.fps_display.draw()
        # swap the double buffer
        self.win.flip()
