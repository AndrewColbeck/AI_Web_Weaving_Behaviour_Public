from copy import deepcopy
from Models import WorldState


class GOAPController(object):

    def choose_action(self, goals=None, actions=None, max_depth=3):
        # save current state of goals
        goals = deepcopy(goals)
        actions = deepcopy(actions)

        world_state = WorldState(goals=goals, actions=actions)

        states = [[world_state, next(
            filter(lambda action: action.name == "seek", world_state.actions))]]

        best_action = None
        best_value = 100000  # High to start
        best_plan = []

        verbose = False

        if verbose:
            print("Searching ...")

        changed = True

        while states:
            current_value = states[-1][0].state_discontentment()

            if verbose and changed:
                text_indent = "   " * len(states)
                print(text_indent + "'->" + states[-1][1].name +
                      " (" + str(states[-1][0].state_discontentment()) + ")")

            if len(states) >= max_depth:
                # if current value is best (low) keep it!
                if current_value < best_value:
                    best_value = current_value
                    best_plan = [state[1]
                                 for state in states if state[1]] + [best_value]
                states.pop()
                continue

            next_action = states[-1][0].next_action()

            if next_action:
                # clone current world states to modify with action
                # use deep copy instead of ref just in case!
                new_state = deepcopy(states[-1][0])
                states.append([new_state, None])
                states[-1][1] = next_action

                # apply action
                new_state.reset()
                states[-1][0].apply_action(next_action)
                changed = True
            else:
                changed = False
                states.pop()

        if verbose:
            print("----------")
            print("BEST PLAN: ", end=' ')
            print(best_plan[1].name, end=' ')
            for i in range(2, len(best_plan)-1):
                print(", " + best_plan[i].name, end=' ')
            print("("+str(best_plan[len(best_plan)-1])+")")
            print(' ')

        return best_plan[1]  # first action in best plan sequence
