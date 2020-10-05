from .component import Component
from SwinModules import Vector2D, Path
from random import random, randrange, uniform
from math import sin, cos, radians
from Models.forces import *

MOVABLE = 'Movable'


class Movable(Component):
    def __init__(self, parent=None, world=None, mass=1.0, scale=10.0, forces=None):
        self.parent = parent
        self.world = world
        self.type = MOVABLE
        self.forces = forces
        self.vel = Vector2D()
        self.force = Vector2D()  # current steering force

        self.accel = Vector2D()  # current acceleration due to force
        self.mass = mass
        # path to follow
        self.path = Path(4, 50, self.world.cy/2,
                         self.world.cx-50, self.world.cy/2)
        self.waypoint_threshold = 30
        self.target = Vector2D(
            self.world.cx / 2, self.world.cy / 2)

        # wander details
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 0.5 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale

    def calculate(self, action, delta):
        if action.name == 'seek':
            force = self.follow_path()
        if action.name == 'fly':
            force = self.move_in_circles(delta)
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, action, delta):
        force = self.calculate(action, delta)
        force.truncate(self.forces[MAX_FORCE])

        # determin the new accelteration
        self.accel = force / self.mass  # not needed if mass = 1.0
        # new velocity
        self.vel += self.accel * delta
        # check for limits of new velocity
        self.vel.truncate(self.forces[MAX_SPEED])
        # update position
        self.parent.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.parent.heading = self.vel.get_normalised()
            self.parent.side = self.parent.heading.perp()

        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.parent.pos)

    def move_in_circles(self, delta):
        ''' Random wandering using a projected jitter circle. '''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta  # this time slice
        # first, add a small random vector to the target's position
        wt += Vector2D(uniform(-1, 1) * jitter_tts,
                       uniform(-1, 1) * jitter_tts)

        # re-project this new vector back on to a unit circle
        wt.normalise()
        # increase the length of the vector to the same as the radius
        # of the wander circle
        wt *= self.wander_radius
        # move the target into a position WanderDist in front of the agent
        # target = wt + Vector2D(self.wander_dist, 0)
        target = self.parent.pos + Vector2D(uniform(1, 5), uniform(1, 5))
        # project the target into world space
        wld_target = self.world.transform_point(
            target, self.parent.pos, self.parent.heading, self.parent.side)
        # and steer towards it
        return self.seek(wld_target)

    def follow_path(self):
        # If heading to final point (is_finished?),
        if self.path.is_finished():
            # Return a slow down force vector (Arrive)
            return self.arrive(self.path.current_pt(), DECEL_SLOW)

        elif (self.path.current_pt() - self.parent.pos).length() < self.waypoint_threshold:
            # If within threshold distance of current way point, inc to next in path
            self.path.inc_current_pt()
        else:
            # Return a force vector to head to current point at full speed (Seek)
            return self.seek(self.path.current_pt())

        return Vector2D()

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.parent.pos).normalise() * \
            self.forces[MAX_SPEED]
        return (desired_vel - self.vel)

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.forces[speed]
        to_target = target_pos - self.parent.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.forces[MAX_SPEED])
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def get_x(self):
        return self.pos.x

    def get_y(self):
        return self.pos.y
