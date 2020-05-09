import sys

from prepareEnvironment import prepare_environment
from solver import solve


def main():
    # w pierwszym kroku interpretujemy plik z podanym celem, stanem, akcjami
    environment = prepare_environment(None)
    print("\nState: ")
    print(environment.state)

    print("\nActions: ")
    print(environment.actions)

    goal = environment.goals.pop()
    print("\nGoal: " + str(goal))

    print("\nLiterals: ")
    print(environment.literals)

    # # Cel jest osiagniety na starcie ?
    # goal_achieved = environment.goal_achieved()

    # if not goal_achieved:
    #     print("Trying to solve...")

    #     analysis = sys.argv[1]

    #     # wywolujemy solver na zainicjalizowanym srodowisku
    #     problem_solved = solve(environment, analysis)

    #     if problem_solved is None:
    #         print("Problem not solved.")
    #     else:
    #         print("Problem solved!")
    #         print_plan(problem_solved)
    # else:
    #     print("Problem solved! Goal achieved at start")


if __name__ == "__main__":
    main()
