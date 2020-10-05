# from .Libraries.vector2d import Vector2D
# from .Libraries.matrix33 import Matrix33
# from .Libraries.graphics import egi

from SwinModules import egi, Vector2D, Matrix33


class World(object):

    def __init__(self, config):
        self.config = config
        self.cx = config["world size"][0]
        self.cy = config["world size"][1]
        self.target = Vector2D(
            config["world size"][0] / 2, config["world size"][1] / 2)
        self.hunter = None
        self.moths = {}
        self.paused = False
        self.show_info = True
        self.verbose = config["verbose"]

    def update(self, delta):
        if not self.paused:
            pass

    def render(self):
        if self.show_info:
            pass
            # infotext = ', '.join(set(str(self.moths[id].pos for id in self.moths))
            # egi.white_pen()
            # egi.text_at_pos(0, 0, infotext)

    def wrap_around(self, pos):
        ''' Treat world as a toroidal space. Updates parameter object pos '''
        max_x, max_y = self.cx, self.cy
        if pos.x > max_x:
            pos.x = pos.x - max_x
        elif pos.x < 0:
            pos.x = max_x - pos.x
        if pos.y > max_y:
            pos.y = pos.y - max_y
        elif pos.y < 0:
            pos.y = max_y - pos.y

    def transform_points(self, points, pos, forward, side, scale):
        ''' Transform the given list of points, using the provided position,
            direction and scale, to object world space. '''
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts

    def transform_point(self, point, pos, forward, side):
        ''' Transform the given single point, using the provided position,
        and direction (forward and side unit vectors), to object world space. '''
        # make a copy of the original point (so we don't trash it)
        wld_pt = point.copy()
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform the point (in place)
        mat.transform_vector2d(wld_pt)
        # done
        return wld_pt
