from Action import Action

# funkcje  pomocnicze


def concatenate_list(l):
    return ", ".join([str(s) for s in l])


class ParsedAction:
    def __init__(self, name, params, preconditions, effects):
        self.name = name
        self.params = params
        self.preconditions = preconditions
        self.effects = effects

   # parsujemy akcje wyciagnieta z pliku
    def transform(self, environment):
        self.transforms = []
        current_literals = []
        self.transform_helper(environment.literals,
                              current_literals, self.transforms)

    def transform_helper(self, all_literals, current_literals, transforms):
        if len(current_literals) == len(self.params):

            zipped_params = dict(zip(self.params, current_literals))
            transformed_preconditions = [precondition.transform(
                zipped_params) for precondition in self.preconditions]
            transformed_effects = [effect.transform(
                zipped_params) for effect in self.effects]
            transforms.append(Action(self, current_literals,
                                     transformed_preconditions, transformed_effects))
            return

        for literal in all_literals:
            if literal not in current_literals:
                self.transform_helper(
                    all_literals, current_literals + [literal], transforms)

    def print_transforms(self):
        i = 0
        for transform in self.transforms:
            print("transforming " + str(i))
            print(transform)
            print("")
            i = i + 1

    # czytelna forma  do wypisywania na konsoli
    def __str__(self):
        return "{0}({1})\nPre: {2}\nPost: {3}".format(self.name, concatenate_list(self.params), concatenate_list(self.preconditions), concatenate_list(self.effects))
