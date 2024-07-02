from numbers import Number
from typing import List, Dict
from eq_parser import parse


class Solver:
    """Solve polynomial equation of degree <= 2

    Accepts only positive integers exponents
    """

    def __init__(self) -> None:
        pass

    def reduce(self, terms: Dict[int, float], degree: int) -> str:
        """Simplify an equation

        Args:
            terms (Dict[int, float]): terms (exp : mul)
            degree (int): degree of the equation

        Returns:
            str: simplified equation
        """

        if not terms:
            return "0 = 0"
        reduced = ""
        for exp in range(degree + 1):
            if exp in terms:
                mul = terms[exp]
                if mul == 0.0:
                    continue
                if reduced:
                    reduced += ' '
                if reduced and mul >= 0:
                    reduced += '+ '
                reduced += str(mul).removesuffix(".0")
                if exp > 0:
                    reduced += " * X"
                    if exp > 1:
                        reduced += f"^{exp}"
        reduced = reduced.replace('-', "- ")
        if reduced.startswith("- "):
            reduced = '-' + reduced[2:]
            reduced = reduced.replace("- ", '-', 1)
        reduced += " = 0"
        return reduced

    def solve(self, equation: str, display: bool) -> List[Number] | None:
        """Solve an equation

        Works for degree < 3
        Compute the reduced form in self.reduced

        Args:
            equation (str): equation to solve
            display (bool): display intermediate steps

        Returns:
            List[Number] | None: the solutions or None if no solution (empty = any number is solution)
        """

        if display: # TODO Finish
            print("First parse the equation")

        parsed = parse(equation)
        self.degree = max(parsed) if parsed else 0
        self.reduced = self.reduce(parsed, self.degree)
        a = parsed.get(2, 0.0)
        b = parsed.get(1, 0.0)
        c = parsed.get(0, 0.0)
        self.delta = b * b - 4 * a * c

        solutions = []
        if self.degree == 0:
            return None if parsed else []
        elif self.degree == 1:
            solutions.append(-c / b)
        elif self.degree == 2:
            if self.delta > 0:
                solutions.append((-b + self.delta**.5) / (2 * a))
                solutions.append((-b - self.delta**.5) / (2 * a))
            elif self.delta < 0:  # Complex solutions
                solutions.append((-b + 1j * (-self.delta)**.5) / (2 * a))
                solutions.append((-b - 1j * (-self.delta)**.5) / (2 * a))
            else:
                solutions.append(-b / (2 * a))

        return solutions


def main() -> None:
    """Tests the equation reducer"""

    # Reducer tests
    tests = [
        ("1 + 2 + 3", "6 = 0"),
        ("1 + 2 + 3 * X^0", "6 = 0"),
        ("1 + 2 + 3 * X", "3 + 3 * X = 0"),
        ("1 + 2 * X ^ 1 + 3 * X", "1 + 5 * X = 0"),
        ("1 + 2 * X ^ 1 + 3 * X - 3 * X ^ 0", "-2 + 5 * X = 0"),
        ("1 + 2 * X ^ 1 + 3 * X - 7 * X ^ 2", "1 + 5 * X - 7 * X^2 = 0"),
        ("-5 * X + 1 + 2 * X ^ 1 + 3 * X - 7 * X ^ 2", "1 - 7 * X^2 = 0"),
        ("-5 * X ^ 8 + 1 + 2 * X ^ 1 + 3 * X - 7 * X ^ 2", "1 + 5 * X - 7 * X^2 - 5 * X^8 = 0"),
        ("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0", "4 + 4 * X - 9.3 * X^2 = 0"),
    ]

    solver = Solver()
    for eq, p in tests:
        solver.solve(eq)
        res = solver.reduced
        if res != p:
            print("Failed for", eq)
            print("Found   :", res)
            print("Expected:", p)
            print()


if __name__ == "__main__":
    main()
