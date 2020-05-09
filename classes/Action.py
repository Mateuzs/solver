# funkcje pomocnicze


def concatenate_list(l):
    return ", ".join([str(s) for s in l])


def cond_contains(items, target):
    for item in items:
        if cond_match(item, target):
            return True
    return False


def cond_find(items, target):
    for item in items:
        if cond_match(item, target):
            return item
    return None


def cond_match(ground1, ground2):
    # sprawdzamy czy warunek ma te sama nazwe i literaly
    if ground1.predicate != ground2.predicate:
        return False
    if len(ground1.literals) != len(ground2.literals):
        return False
    for i, j in zip(ground1.literals, ground2.literals):
        if i != j:
            return False
    return True


class Action:
    def __init__(self, action, literals, preconditions, effects):
        self.action = action
        self.literals = literals
        self.preconditions = preconditions
        self.effects = effects

        # jezeli warunek wykonania definiuje cos co nie bedzie zmienione w efekcie to zostanie dodany razem
        # z  effektem do zbioru kompletnych efektow

        self.complete_effects = list(effects)
        for precondition in preconditions:
            if not cond_contains(self.complete_effects, precondition):
                self.complete_effects.append(precondition)

    # czytelna forma do wypisywania na konsoli
    def __str__(self):
        return "{0}({1})\nPre: {2}\nPost: {3}".format(self.action.name, concatenate_list(self.literals), concatenate_list(self.preconditions), concatenate_list(self.effects))

    # forma uproszczona
    def simple_str(self):
        return "{0}({1})".format(self.action.name, concatenate_list(self.literals))
