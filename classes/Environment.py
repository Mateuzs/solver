# funkcja parsujaca plik z opisem w jezyku STRIPS

from classes.Condition import Condition

# funkcje pomocnicze


def concatenate_list(l):
    return ", ".join([str(s) for s in l])


class Environment:
    def __init__(self):
        self.actions = dict()
        self.goals = set()
        self.state = dict()
        self.literals = set()

    # dodajemy cel do zbioru celi
    def add_goal(self, predicate, literals, truth=True):
        condition = Condition(predicate, literals, truth)
        self.goals.add(condition)

    # dodajemy literal do zbioru znanych literalow
    def add_literal(self, literal):
        self.literals.add(literal)
    # dodajemy akcje

    def add_action(self, action):
        if action.name not in self.actions:
            self.actions[action.name] = action

    # dodajemy do stanu prawdziwy predykat
    def set_true(self, predicate, literals):
        if predicate not in self.state:
            self.state[predicate] = set()
        self.state[predicate].add(literals)

    # usuwamy ze stanu nieprawdziwy predykat
    def set_false(self, predicate, literals):
        if predicate in self.state:
            self.state[predicate].remove(literals)

    # sprawdzamy czy predykat jest prawdziwy
    def is_true(self, predicate, literals):
        if predicate not in self.state:
            return False
        return literals in self.state[predicate]

    # sprawdzamy czy predykat nie jest prawdziwy
    def is_false(self, predicate, literals):
        return not self.is_true(predicate, literals)

    # sprawdzamy osiagniecie celu
    def goal_achieved(self):
        for goal in self.goals:
            if not goal.achieved(self):
                return False
        return True
