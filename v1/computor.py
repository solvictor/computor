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
        print(f"{solutions=}")
        print("Reduced form:", solver.reduced)
        print("Polynomial degree:", solver.degree)
        if solver.degree > 2:
            print("The polynomial degree is strictly greater than 2, I can't solve.")
        elif solutions is None:
            # "2 * X^0 = 0" - No solution
            print("There is no solution")
        elif len(solutions) == 0:
            # "2 * X^0 = 2 * X^0" - Any number
            print("Any real number is a solution")
        else:
            if solver.delta == 0:
                print("Discriminant is zero, the solution is:")
            else:
                print(f"Discriminant is strictly {"positive" if solver.delta > 0 else "netagive"}, the two solutions are:")
            print(*solutions, sep='\n')

    except Exception as ex:
        print(ex, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
