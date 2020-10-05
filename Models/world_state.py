
from Models import Goal, Action


class WorldState():
    def __init__(self, goals=None, actions=None):
        self.goals = goals
        self.actions = actions
        self.action_index = -1

    def state_discontentment(self):
        discontentment = 0

        for goal in self.goals:
            discontentment += goal.getGoalValue()

        return discontentment

    def next_action(self):
        for i in range(self.action_index + 1, len(self.actions)):
            self.action_index = i
            return self.actions[i]

        return None

    def reset(self):
        self.action_index = -1

    def apply_action(self, action):

        for effect_key in action.effects.keys():
            for goal in self.goals:
                if goal.name is effect_key:
                    goal.updateGoalValue(action.effects[effect_key])
