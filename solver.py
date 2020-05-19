from classes.Condition import Condition

from utils import find, match, deep_match, is_dangerous, initial_state_count, action_satisfied, precondition_reachable, preconditions_reachable, update_state, get_possible_actions

# glowna funkcja rozwiazujaca


def solve(environment, analysis, max_depth):
    state = []

    for predicate in environment.state:
        for literals in environment.state[predicate]:
            state.append(Condition(predicate, literals, True))

    goals = list(environment.goals)
    b_analysis = False if analysis == "false" else True

    return solve_lvl(environment, state, goals, [], 0, max_depth, b_analysis)


def solve_lvl(environment, state, goals, current_plan, depth, max_depth, analysis):
    padding = "".join(["**" for x in range(0, len(current_plan))]) + " "
    plan = []

    if analysis:
        print("Current Plan: {0}".format(
            "\n".join([x.simple_str() for x in current_plan])))
        print("\n###############################\n")

    if len(goals) == 0:
        return plan

    if depth > max_depth:
        return None

    i = 0
    while i < len(goals):
        goal = goals[i]

        if analysis:
            print padding + "Current Plan: {0}".format(" -> ".join([x.simple_str() for x in current_plan]))
            print padding + "Subgoal: {0}".format(goal)
            print padding + "Other Goals: {0}".format(", ".join([str(x) for x in goals[i+1:]]))
            print padding + "State: {0}".format(", ".join([str(s) for s in state]))
            raw_input("")

        if action_satisfied(state, goal):
            # recurse
            if analysis:
                raw_input(padding + "Goal is already satisfied!")
                print ""
            i += 1
            continue

        possible_actions = sorted(get_possible_actions(
            environment, goal), key=lambda c: initial_state_count(state, c.preconditions))

        # musimy znalesc podcel ktory pomoze nam osiagnac cel

        # znajdz wszystkie akcje ktore moga osiagnac cel
        if analysis:
            print padding + "set of possible actions which reach goal: {0}:".format(goal)
            print "\n".join([padding + x.simple_str() for x in possible_actions])
            raw_input("")

        action_found = False

        for action in possible_actions:

            if analysis:
                print padding + "Trying next action to reach goal:  {0}:".format(goal)
                print padding + str(action).replace("\n", "\n" + padding)
                raw_input("")

            # sprawdza czy jest przynajmniej jedna akcja dla kazdego warunku ktora osiaga go
            if not preconditions_reachable(environment, action):
                if analysis:
                    print padding + "Some preconditions not reachable by any possible action. Have to skip"
                    raw_input("")
                continue

            # sprawdza czy jakas akcja zagraza innemu celowi
            if is_dangerous(goals, action):
                if analysis:
                    print padding + "Action threaten another goal state. Have to skip"
                    raw_input("")
                continue

            # jezeli akcja nie moze byc od razu odrzucona jako nieosiagalna, obnizaj
            if analysis:
                print padding + "Action cannot be rejected as unreachable. Have to descend..."
                raw_input("")

            temporary_state = list(state)

            subgoals = list(action.preconditions)

            current_plan.append(action)

            solution = solve_lvl(
                environment, temporary_state, subgoals, current_plan, depth + 1, max_depth, analysis)

            # jezeli nie znaleziono rozwiazania
            if solution is None:
                if analysis:
                    print padding + "No solution found with this action. Have to skip..."
                current_plan.pop()
                continue

            if analysis:
                print padding + "Possible solution found!"
                raw_input("")

            # aktualizacja stanu o efekt ktory wprowadza nowa akcja
            for effect in action.effects:
                update_state(temporary_state, effect)

            # sprawdza czy stan nie usunal jakiegos z poprzednich podceli
            deleted = [x for x in goals[0:i] if x !=
                       goal and not action_satisfied(temporary_state, x)]
            deleted_length = len(deleted)
            if len(deleted) > 0:

                if analysis:
                    print padding + "reach {0} but delete other goals: {1}".format(goal, ", ".join([str(x) for x in deleted]))
                    print padding + "Re-adding the deleted goals to the end of the list"
                    raw_input("")
                [goals.remove(x) for x in deleted]
                [goals.append(x) for x in deleted]
                i -= deleted_length

                if analysis:
                    print padding + "New goals: {0}".format(", ".join([str(x) for x in goals]))
                    raw_input("")

            # dodaj podcel do celi
            plan.extend(solution)

            # akceptuj tymczasowy stan
            del state[:]
            state.extend(temporary_state)

            # dodaj akcje do planu
            plan.append(action)

            if analysis:
                print padding + "New State: " + ", ".join([str(x) for x in state])
                raw_input("")

            i += 1
            action_found = True
            break

        if not action_found:
            if analysis:
                print ""
                raw_input(
                    "**" + padding + "No actions found to reach this subgoal. Go back...")
                print ""

            return None

    return plan


def print_plan(plan):
    print "Plan: {0}".format(" -> ".join([x.simple_str() for x in plan]))
