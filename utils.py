
# Funkcje pomocnicze


def find(items, target):
    for item in items:
        if match(item, target):
            return item
    return None


def match(condition1, condition2):
    if condition1.predicate != condition2.predicate:
        return False
    if len(condition1.literals) != len(condition2.literals):
        return False
    for i, j in zip(condition1.literals, condition2.literals):
        if i != j:
            return False
    return True


def deep_match(condition1, condition2):

    return condition1.truth == condition2.truth and match(condition1, condition2)


def is_dangerous(state, action):
    for effect in action.effects:
        threat = find(state, effect)
        if threat != None and threat.truth != effect.truth:
            return True
    return False


def initial_state_count(state, preconditions):
    count = 0
    for precondition in preconditions:
        if not action_satisfied(state, precondition):
            count += 1
    return count


def action_satisfied(state, goal):
    condition = find(state, goal)

    # sledzimy tylko pozytywne literaly, wiec jak tu jest to znaczy ze prawda
    if goal.truth == True:
        return condition != None

    return condition == None


def preconditions_reachable(environment, action):
    for precondition in action.preconditions:
        if not precondition_reachable(environment, precondition):
            return False

    return True


def precondition_reachable(environment, precondition):
    if precondition.achieved(environment):
        return True

    for key, action in environment.actions.iteritems():
        for transform in action.transforms:
            for effect in transform.effects:
                if deep_match(effect, precondition):
                    return True
    return False


def update_state(state, effect):
    # szukamy warunku pozytywnego lub negatywnego w stanie
    condition = find(state, effect)

    # jezeli warunek nie istnieje a efekt jest pozytywny, dodajemy
    if effect.truth == True:
        if condition is None:
            state.append(effect)
    # jezeli warunek istnieje a effekt ma negatywny znak, usuwamy
    elif condition != None and effect.truth is False:
        state.remove(condition)


def get_possible_actions(environment, goal):
    results = []
    for key, action in environment.actions.iteritems():
        for transform in action.transforms:
            for effect in transform.effects:
                if deep_match(effect, goal):
                    results.append(transform)
                    break
    return results
