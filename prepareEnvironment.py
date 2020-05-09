import re
import sys
import fileinput

from classes.Environment import Environment
from classes.ParsedAction import ParsedAction
from classes.ParsedCondition import ParsedCondition


class ParseStage:
    INIT = 0
    GOAL = 1
    ACTIONS = 2
    ACTION_STATEMENT = 3
    PRECONDITIONS = 4
    EFFECTS = 5


def prepare_environment(filename):
    # tworzymy nowa klase srodowiska
    environment = Environment()

    # pomocnicze regexy do parsowania pliku

    initialStateRegex = re.compile('init:', re.IGNORECASE)

    goalStateRegex = re.compile('goal:', re.IGNORECASE)

    # dopasowuje predykat NawaPredykatu(literal), !NazwaPredykatu(literal)
    predicateRegex = re.compile(
        '(!?[A-z][a-zA-z_]*) *\( *([a-zA-z0-9_, ]+) *\)')

    actionStateRegex = re.compile('actions:', re.IGNORECASE)

    preconditionsRegex = re.compile('preconditions:', re.IGNORECASE)

    effectsRegex = re.compile('effects:', re.IGNORECASE)

    # definiujemy etap parsowania pliku, wszystkie mozliwe etapy definiuje klasa ParseState
    parseStage = ParseStage.INIT

    current_action = None

    if filename is None:
        filename = sys.argv[1]

    # Parsowanie pliku
    with open(filename) as file:
        for line in file:
            # oczyszczamy linie i sprawdzamy czy jest pusta badz komentarzem
            if line.strip() == "" or line.strip()[:2] == "//":
                continue

            if parseStage == ParseStage.INIT:
                # parsujemy stan poczatkowy z linii tekstu
                initState = initialStateRegex.match(line)

                # Sprawdzamy poprawnosc definicji stanu poczatkowego
                if initState is None:
                    raise Exception(
                        "init state not defined properly. Line should start with 'init: '")

                # znajdujemy wszystkie predykaty stanu poczatkowego
                predicates = re.findall(
                    predicateRegex, line[len(initState.group(0)):].strip())

                for predicate in predicates:
                    # wyciagamy nazwe predykatu
                    name = predicate[0]
                    # wyciagamy literaly wewnatrz predykatu
                    literals = tuple([literal.strip()
                                      for literal in predicate[1].split(",")])
                    # wpisujemy literaly do znanych literalow srodowiska
                    for literal in literals:
                        environment.add_literal(literal)

                    # aktualizujemy stan srodowiska
                    if name[0] == '!':
                        name = name[1:]
                        environment.set_false(name, literals)
                    else:
                        environment.set_true(name, literals)

                parseStage = ParseStage.GOAL

            elif parseStage == ParseStage.GOAL:
                # parsujemy cel z linii
                goal = goalStateRegex.match(line)

                # sprawczamy poprawnosc definicji celu
                if goal is None:
                    raise Exception(
                        "goal state not defined properly. Line should start with 'goal: '")

                # wyciagamy wszystkie predyaty celu
                predicates = re.findall(
                    predicateRegex, line[len(goal.group(0)):].strip())

                for predicate in predicates:
                    # wyciagamy nazwe predykatu
                    name = predicate[0]

                    # wyciagamy literaly wewnatrz srodowiska
                    literals = tuple([literal.strip()
                                      for literal in predicate[1].split(",")])

                    # aktualizujemy zbior znanych literalow srodowiska
                    for literal in literals:
                        environment.add_literal(literal)

                    # sprawdzamy czy predykat jest zanegowany
                    truth = name[0] != '!'

                    # jesli tak, aktualizujemy jego nazwe
                    if not truth:
                        name = name[1:]

                    # Dodajemy warunek osiagniecia celu
                    environment.add_goal(name, literals, truth)

                parseStage = ParseStage.ACTIONS

            elif parseStage == ParseStage.ACTIONS:
                # parsujemy mozliwe akcje do wykonania z pliku
                actions = actionStateRegex.match(line)

                # sprawdzamy poprawnosc definicji
                if actions is None:
                    raise Exception(
                        "Actions not defined properly. Line should start with 'actions: '")

                parseStage = ParseStage.ACTION_STATEMENT

            elif parseStage == ParseStage.ACTION_STATEMENT:

                # Definicja akcji bedzie tak definiowana jak predykat
                action = predicateRegex.match(line.strip())

                if action is None:
                    raise Exception(
                        "Action not defined properly.  action should be like: Name(Param1, ...)")

                # wyciagamy nazwe akcji
                name = action.group(1)
                # wyciagamy parametry akcji
                params = tuple([param.strip()
                                for param in action.group(2).split(",")])

                # zapisujemy obecna akcje
                current_action = ParsedAction(name, params, [], [])

                parseStage = ParseStage.PRECONDITIONS

            elif parseStage == ParseStage.PRECONDITIONS:

                # Warunek zapisany jest tak jak stan poczatkowy, ale rozni sie poczatkiem linii
                preconditions = preconditionsRegex.match(line.strip())

                # Sprawdzamy poprawnosc definicji warunkow
                if preconditions is None:
                    raise Exception(
                        "Preconditions not defined properly. Line should start with 'Preconditions: ' ")

                # wyciagamy predykaty
                predicates = re.findall(
                    predicateRegex, line[len(preconditions.group(0)):].strip())

                for predicate in predicates:
                    # wyciagamy nazwe predykatu
                    name = predicate[0]

                    params = tuple([param.strip()
                                    for param in predicate[1].split(",")])

                    # warunki moga miec literaly ktore dopiero beda deklarowane
                    for param in params:
                        if param not in current_action.params:
                            environment.add_literal(param)

                    # sprawdzamy czy predykat jest zanegowany
                    truth = name[0] != '!'

                    # jesli jest, aktualizujemy nazwe
                    if not truth:
                        name = name[1:]

                    current_action.preconditions.append(
                        ParsedCondition(name, params, truth))

                parseStage = ParseStage.EFFECTS

            elif parseStage == ParseStage.EFFECTS:
                # efekty zdefiniowane podobnie jak stan, roznia sie poczatkiem linii
                effects = effectsRegex.match(line.strip())

                # sprwadzamy pooprawnosc definicji efektow
                if effects is None:
                    raise Exception(
                        "Effects not defined properly. The line should start with: 'Effects: '")

                # wyciagamy efekty
                predicates = re.findall(
                    predicateRegex, line[len(effects.group(0)):].strip())

                for predicate in predicates:
                    # wyciagamy nazwe predykatu
                    name = predicate[0]

                    params = tuple([param.strip()
                                    for param in predicate[1].split(",")])

                    # efekty moga miec literaly ktore dopiero beda deklarowane
                    for param in params:
                        if param not in current_action.params:
                            environment.add_literal(param)

                    # sprawdzamy czy predykat nie jest zanegownay
                    truth = name[0] != '!'

                    # jesli tak, aktualizujemy nazwe
                    if not truth:
                        name = name[1:]

                    current_action.effects.append(
                        ParsedCondition(name, params, truth))

                # Dodajemy akcje do srodowiska
                environment.add_action(current_action)

                parseStage = ParseStage.ACTION_STATEMENT

    for _name, parsedAction in environment.actions.iteritems():
        parsedAction.transform(environment)

    return environment
