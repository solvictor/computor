import sys
from solver import Solver


# TODO Read from stdin if no input ?
def main() -> None:
    args = sys.argv

    if len(args) != 2:
        print("Usage: python3 computer.py <equation>", file=sys.stderr)
        exit(1)

    equation = args[1]
    solver = Solver()
    try:
        solutions = solver.solve(equation)
        print("Reduced form:", solver.reduced)
        print("Polynomial degree:", solver.degree)
        if solver.degree > 2:
            print("The polynomial degree is strictly greater than 2, I can't solve.")
        elif solutions is None:
            print()
        print(solutions)
    except Exception as ex:
        print(ex, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
