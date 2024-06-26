import sys
from solver import Solver


# TODO Read from stdin if no input ?
def main() -> None:
    args = sys.argv

    if len(args) != 2:
        print("Usage: python3 computer.py <equation>", file=sys.stderr)
        exit(1)

    equation = args[1]
    solver = Solver(equation)
    try:
        solutions = solver.solve()

        print(solutions)
    except Exception as ex:
        print(ex, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
