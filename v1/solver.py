from numbers import Number
from typing import List, Dict


def next_index(string: str, charset: str, start: int):
    for i in range(start, len(string)):
        if string[i] in charset:
            return i
    return -1


def parse_exp(string: str) -> int:
    if not string.startswith('X'):
        raise SyntaxError(f"Invalid equation: '{string}' is unrecognized")

    if len(string) == 1:
        return 1

    if string[1] != '^':
        raise SyntaxError(f"Invalid equation: '{string}' is unrecognized")

    exp = string[2:]
    if not exp.isdigit():
        raise SyntaxError(f"Invalid equation: '{exp}' should be an integer")

    return int(exp)


"-5.923 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
# Should return same as
"-6.923*X^0+4*X^1-9.3*X^2"
"-6.923+4*X^1-9.3*X^2"


def parse_poly(polynom: str) -> Dict[int, float]:
    if not polynom:
        raise SyntaxError(f"Invalid equation: polynom is empty")

    parsed = {}  # exp: mul

    i = 0
    while i < len(polynom):
        end = next_index(polynom, "+-", i + 1)
        if end == -1:
            end = len(polynom)

        part = polynom[i:end]
        mul = 1.0
        exp = 0

        times = part.count("*")
        if times > 1:
            raise SyntaxError(f"Invalid equation: too many '*' in '{part}'")
        if times == 1:
            m, e = part.split('*')
            try:
                mul = float(m)
            except Exception:
                raise SyntaxError(f"Invalid equation: '{m}' should be a valid float")
            exp = parse_exp(e)
        else:
            try:
                mul = float(part)
            except Exception:
                exp = parse_exp(part)

        # print(f"{part}   {mul = }   {exp = }")
        parsed[exp] = parsed.get(exp, 0.0) + mul
        i = end

    return parsed


class Solver:

    def __init__(self, equation: str) -> None:
        self.equation = equation.upper()

    def _parse(self) -> Dict[int, float]:
        equation = ''.join(c for c in self.equation if not c.isspace())

        if not equation:
            raise SyntaxError("Invalid equation: equation is empty")

        equals = equation.count("=")
        if equals > 1:
            raise SyntaxError("Invalid equation: more than one '=' found")
        elif equals == 0:  # TODO Maybe invalid too
            equation += "=0"

        left, right = equation.split("=")
        parsed = parse_poly(left)

        for exp, mul in parse_poly(right).items():
            parsed[exp] = parsed.get(exp, 0.0) - mul

        return parsed

    def solve(self) -> List[Number]:
        parsed = self._parse()
        degree = max(parsed)
        print(f"{parsed = } {degree = }")
        return []
