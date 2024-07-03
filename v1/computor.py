import sys
from solver import Solver
from sol_formatter import format_sol
from argparse import ArgumentParser


def main() -> None:
    """Compute and format the solutions of the input equation"""

    parser = ArgumentParser(
        prog="ComputorV1",
        description="Solve polynomial equation up to degree 2"
    )

    parser.add_argument(
        "equation",
        help="Equation to solve"
    )
    parser.add_argument(
        "-d",
        "--display",
        action="store_true",
        help="Displays intermediate steps"
    )

    args = parser.parse_args()
    solver = Solver()
    try:
        solutions = solver.solve(args.equation, args.display)
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
            if solver.degree == 1:
                print("The solution is:")
            elif solver.delta == 0:
                print("Discriminant is zero, the solution is:")
            else:
                print(f"Discriminant is strictly {"positive" if solver.delta > 0 else "negative"}, the two solutions are:")

            for solution in solutions:
                print(format_sol(solution))

    except Exception as ex:
        print(ex, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
