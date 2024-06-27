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

    def solve(self, equation: str) -> List[Number]:
        parsed = parse(equation)
        self.degree = max(parsed)
        self.reduced = self.reduce(parsed, self.degree)

        # print(f"{parsed = } {degree = }")
        # print(f"{self.reduced = }")
        return []


def main() -> None:
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
