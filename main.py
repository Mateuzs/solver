import sys

from prepareEnvironment import prepare_environment

from solver import solve, print_plan


def main():

    print("\nParsing problem...")
    # w pierwszym kroku interpretujemy plik z podanym celem, stanem, akcjami
    environment = prepare_environment()
    print("\nState: ")
    print(environment.state)

    print("\nActions: ")
    for action in environment.actions:
        print(action)

    print("\nLiterals: ")
    print(environment.literals)

    print("\nGoal: ")
    for goal in environment.goals:
        print(goal)

    print("\n")
    # Cel jest osiagniety na starcie ?
    goal_achieved = environment.goal_achieved()

    if not goal_achieved:
        print("Solving......")

        analysis = sys.argv[2]
        depth = sys.argv[3]

        # wywolujemy solver na zainicjalizowanym srodowisku
        problem_solved = solve(environment, analysis, depth)

        if problem_solved is None:
            print("Problem not solved.")
        else:
            print("\nProblem solved!\n")
            print_plan(problem_solved)
    else:
        print("Problem solved! Goal achieved at start")


if __name__ == "__main__":
    main()
