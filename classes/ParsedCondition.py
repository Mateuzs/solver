from classes.Condition import Condition

# funkcje pomocnicze


def concatenate_list(l):
    return ", ".join([str(s) for s in l])


class ParsedCondition:
    def __init__(self, predicate, params, truth=True):
        self.predicate = predicate
        self.params = params
        self.truth = truth

    # transformacja sparsowanego warunku
    def transform(self, args_map):
        args = list()
        for param in self.params:
            if param in args_map:
                args.append(args_map[param])
            else:
                args.append(param)
        return Condition(self.predicate, tuple(args), self.truth)

    # czytelna forma do wypisania w konsoli
    def __str__(self):
        name = self.predicate
        if not self.truth:
            name = "!" + name
        return "{0}({1})".format(name, concatenate_list(self.params))
