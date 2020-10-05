from SwinModules import Path, Vector2D, Point2D
from Models.influence_map import Node
from copy import deepcopy
from random import randrange


class WebController(object):
    def __init__(self, world):
        self.verbose = False
        self.world = world
        self.resolution = 20
        self.webs = {}

    def add_web(self, web):
        self.webs[web.id] = web

    def add_strand(self, web, node1, node2):
        # deep copy to avoid changing influence_map coords
        a = deepcopy(node1.pos)
        b = deepcopy(node2.pos)

        # Calculate direction of a + b
        c = (b - a)
        # normalise to a vector unit
        c.normalise()

        if self.verbose:
            print("vector a is ", str(a))
            print("vector b is ", str(b))
            print("vector c is ", str(c))

        # increase magnitude until pos2 intersects with edge of map
        while b.y < self.world.cy and b.y > 0:
            if b.x > self.world.cx or b.x < 0:
                break
            b += c

        # increase magnitude in opposite direction until pos1 intersects with edge of map
        while a.y < self.world.cy and a.y > 0:
            if a.x > self.world.cx or a.x < 0:
                break
            a -= c

        # normalise to integers to avoid flops
        a.y = int(a.y)
        a.x = int(a.x)
        b.y = int(b.y)
        b.x = int(b.x)

        if self.verbose:
            print(str(self.world.cy))
            print("start point is ", str(a.x), ", ", str(a.y))
            print("final point is ", str(b.x), ", ", str(b.y))

        # Append the strand to the web
        web.strands.append(
            Path(self.resolution, a.x, a.y, b.x, b.y))

    def render(self):
        for id in self.webs:
            for strand in self.webs[id].strands:
                strand.render()

    def update(self, delta, spiders):
        for id in spiders:
            if spiders[id].web_planning_time_passed >= spiders[id].web_planning_cooldown:
                spiders[id].web_planning_time_passed = 0
                self.plan_web(spiders[id])
            else:
                spiders[id].web_planning_time_passed += delta

    def add_web_between_strand_points(self, web, strand1, strand2):
        longer_strand = strand1
        shorter_strand = strand2

        if strand1._num_pts > strand2._num_pts:
            longer_strand = strand2
            shorter_strand = strand1

        for i in range(0, longer_strand._num_pts, 1):
            node1 = Node(longer_strand._pts[i])
            node2 = Node(shorter_strand._pts[i])
            self.add_interwebbing(web, node1, node2)

    def add_interwebbing(self, web, node1, node2):
        # deep copy to avoid changing influence_map coords
        a = deepcopy(node1.pos)
        b = deepcopy(node2.pos)

        # Append interwebbing
        web.strands.append(
            Path(int(self.resolution/2), a.x, a.y, b.x, b.y))

    def plan_web(self, spider):
        hits = spider.prey_spottings
        if len(hits) <= 1:
            return

        spider.web.strands.clear()

        # Create single strand
        if len(hits) == 2:

            self.add_strand(
                spider.web, hits[0], hits[1])
        # Else try different AI
        else:
            self.plan_creative_web(spider)
            if len(spider.web.strands) >= 2:
                for i in range(0, len(spider.web.strands)-1, 1):
                    self.add_web_between_strand_points(
                        spider.web, spider.web.strands[i], spider.web.strands[i+1])

    def plan_creative_web(self, spider):
        hits = spider.prey_spottings
        web_center = Node(Vector2D())

        for i in range(0, len(hits), 1):
            web_center.pos += hits[i].pos.get_normalised()

        for i in range(1, len(hits), 1):
            self.add_strand(spider.web, web_center, hits[i])
            if i >= 1:
                self.add_interwebbing(spider.web, hits[i], hits[i-1])
