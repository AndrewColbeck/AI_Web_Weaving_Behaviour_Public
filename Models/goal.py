class Goal:
    def __init__(self, name, goal_value):
        self.name = name
        self.goal_value = goal_value

    def getGoalValue(self):
        return self.goal_value

    def getGoalName(self):
        return self.name

    def updateGoalValue(self, change):
        self.goal_value += change

        if self.goal_value < 0:
            self.goal_value = 0
