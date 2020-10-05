from Controllers import GOAPController
from Models import WorldState
from Models.Components import KILLABLE, MOVABLE, RENDERABLE
from Models.spider import SPIDER_ACTIONS, Spider
from Models.influence_map import Node
from SwinModules import Vector2D


class SpiderController(object):
    def __init__(self, world):
        self.world = world
        self.spiders = {}
        self.world_moths = world.moths
        self.goap = GOAPController()
        self.verbose = False
        self.prey_spottings = []

    def add_agent(self, x=None, y=None):
        new_spider = Spider(world=self.world, x=x, y=y)
        self.spiders[new_spider.id] = new_spider
        return new_spider.web

    def update(self, delta):

        for id in self.spiders:
            spider = self.spiders[id]
            spider.time_passed += delta

            if spider.time_passed >= spider.goal_cooldown:
                spider.time_passed = 0
                spider.current_action = self.goap.choose_action(
                    goals=spider.goals, actions=SPIDER_ACTIONS)
                if self.verbose:
                    print("Roar from Spider: ", id)
                    print("NOW I'm gonna ", spider.current_action.name)
                self.apply_action_to_goals(id, spider.current_action)

            self.carry_out_action(spider, delta)

            spider.components[MOVABLE].update(
                spider.current_action, delta)

    def apply_action_to_goals(self, id, action):
        # Apply Action effects to Goals
        for goal in self.spiders[id].goals:
            if self.verbose:
                print(goal.name, str(goal.getGoalValue()))
            if goal.name in action.effects:
                goal.updateGoalValue(action.effects[goal.name])

        # Update my Discontentment
        self.spiders[id].discontentment = WorldState(
            goals=self.spiders[id].goals).state_discontentment()

    def carry_out_action(self, spider, delta):
        if spider.current_action.name == 'sit':
            if spider.moth_last_spotted >= spider.moth_spotting_cooldown:
                spider.moth_last_spotted = 0
                for id in self.world_moths:
                    if spider.pos.distance(self.world_moths[id].pos) < spider.line_of_sight:
                        self.add_prey_spotted(
                            self.world_moths[id].pos.x, self.world_moths[id].pos.y)

                # Decrease influence map over time
                spottings_to_remove = []
                for spotting in spider.prey_spottings:
                    spotting.decrement_hits()
                    if spotting.hits <= 0:
                        spottings_to_remove.append(spotting)

                for spotting in spottings_to_remove:
                    spider.prey_spottings.remove(spotting)

            else:
                spider.moth_last_spotted += delta

    def render(self, delta):
        for id in self.spiders:
            self.spiders[id].components[RENDERABLE].update(delta)

    def add_prey_spotted(self, x, y):
        if len(self.spiders) > 0:
            for id in self.spiders:
                self.spiders[id].prey_spottings.append(Node(Vector2D(x, y)))
