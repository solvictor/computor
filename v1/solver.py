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

    def solve(self, equation: str, display: bool = False) -> List[Number] | None:
        """Solve an equation

        Works for degree < 3
        Compute the reduced form in self.reduced

        Args:
            equation (str): equation to solve
            display (bool): display intermediate steps. Defaults to False.

        Returns:
            List[Number] | None: the solutions or None if no solution (empty = any number is solution)
        """

        if display:
            print("First parse the equation")

        parsed = parse(equation)
        self.degree = max(parsed) if parsed else 0
        self.reduced = self.reduce(parsed, self.degree)
        a = parsed.get(2, 0.0)
        b = parsed.get(1, 0.0)
        c = parsed.get(0, 0.0)
        if display:
            print("Detected degree:", self.degree)

        solutions = []
        if self.degree == 0:
            if display:
                print("Since the degree is 0 there is two case:")
                print(" - Either any rationnal number is a solution")
                print(" - Or there is no solution")
            return None if parsed else []
        elif self.degree == 1:
            if display:
                print("Since the degree is 1 there is one case:")
                print("For an equation a * x + b = 0, the solution is x = -b / a")
                print(f"We have a = {b} and b = {c}")
                print(f"Answer is x = {-c} / {b}")
            solutions.append(-c / b)
        elif self.degree == 2:
            self.delta = b * b - 4 * a * c
            if display:
                print("Since the degree is 2 we need to compute the delta")
                print("For an equation a * x^2 + b * x + c = 0, delta = b^2 - 4 * a * c")
                print(f"We have a = {a}, b = {b} and c = {c}")
                print(f"delta = {b}^2 - 4 * {a} * {c} = {self.delta}")
            if self.delta > 0:
                if display:
                    print("Since delta > 0 there is two real solutions x1 and x2")
                    print(f"x1 = (-b + sqrt(delta)) / (2 * a) = ({-b} + {self.delta**.5}) / {2 * a}")
                    print(f"x2 = (-b - sqrt(delta)) / (2 * a) = ({-b} - {self.delta**.5}) / {2 * a}")
                solutions.append((-b + self.delta**.5) / (2 * a))
                solutions.append((-b - self.delta**.5) / (2 * a))
            elif self.delta < 0:
                if display:
                    print("Since delta < 0 there is two complex solutions x1 and x2")
                    print(f"x1 = (-b + sqrt(-delta)i) / (2 * a) = ({-b} + {1j * (-self.delta)**.5}) / {2 * a})")
                    print(f"x2 = (-b - sqrt(-delta)i) / (2 * a) = ({-b} - {1j * (-self.delta)**.5}) / {2 * a})")
                solutions.append((-b + 1j * (-self.delta)**.5) / (2 * a))
                solutions.append((-b - 1j * (-self.delta)**.5) / (2 * a))
            else:
                if display:
                    print("Since delta = 0 there is one real solution x")
                    print(f"x = -b / (2 * a) = {-b} / {2 * a}")
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
