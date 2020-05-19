# funkcje pomocnicze


def concatenate_list(l):
    return ", ".join([str(s) for s in l])


class Condition:
    def __init__(self, predicate, literals, truth=True):
        self.predicate = predicate
        self.literals = literals
        self.truth = truth

    # sprawdzamy czy warunek osiagnieto
    def achieved(self, environment):
        return environment.is_true(self.predicate, self.literals) == self.truth

    # czytelna forma do wypisania w konsoli
    def __str__(self):
        name = self.predicate
        if not self.truth:
            name = "!" + name
        return "{0}({1})".format(name, concatenate_list(self.literals))
