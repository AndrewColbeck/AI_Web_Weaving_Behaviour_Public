from Controllers import GOAPController
from Models import WorldState
from Models.Components import KILLABLE, MOVABLE, RENDERABLE
from Models.moth import MOTH_ACTIONS, Moth


class MothController(object):
    def __init__(self, world):
        self.verbose = False
        self.world = world
        self.world.moths = {}
        self.goap = GOAPController()

    def add_agent(self, x=None, y=None):
        new_moth = Moth(world=self.world, x=x, y=y)
        self.world.moths[new_moth.id] = new_moth

    def update(self, delta):

        for id in self.world.moths:
            moth = self.world.moths[id]
            moth.time_passed += delta

            if moth.time_passed >= moth.goal_cooldown:
                moth.time_passed = 0
                moth.current_action = self.goap.choose_action(
                    goals=moth.goals, actions=MOTH_ACTIONS)
                self.apply_action_to_goals(id, moth.current_action)

            moth.components[MOVABLE].update(
                moth.current_action, delta)

    def apply_action_to_goals(self, id, action):
        # Apply Action effects to Goals
        for goal in self.world.moths[id].goals:
            if self.verbose:
                print(goal.name, str(goal.getGoalValue()))
            if goal.name in action.effects:
                goal.updateGoalValue(action.effects[goal.name])

        # Update my Discontentment
        self.world.moths[id].discontentment = WorldState(
            goals=self.world.moths[id].goals).state_discontentment()

    def render(self, delta):
        for id in self.world.moths:
            self.world.moths[id].components[RENDERABLE].update(delta)
