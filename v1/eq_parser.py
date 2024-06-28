from typing import Dict


def next_index(string: str, charset: str, start: int = 0) -> int:
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
        raise SyntaxError(f"Invalid equation: '{exp}' must be an integer")

    return int(exp)


def parse_poly(polynom: str) -> Dict[int, float]:
    if not polynom:
        raise SyntaxError("Invalid equation: polynom is empty")

    parsed = {}  # exp: mul

    i = 0
    while i < len(polynom):
        end = next_index(polynom, "+-", i + 1)
        if end == -1:
            end = len(polynom)

        term = polynom[i:end]
        mul = 1.0
        exp = 0

        times = term.count("*")
        if times > 1:
            raise SyntaxError(f"Invalid equation: too many '*' in '{term}'")
        if times == 1:
            m, e = term.split('*')
            try:
                mul = float(m)
            except Exception:
                raise SyntaxError(f"Invalid equation: '{m}' must be a float")
            exp = parse_exp(e)
        else:
            try:
                mul = float(term)
            except Exception:
                if term[0] == '-':
                    mul = -1.0
                if term[0] in "+-":
                    term = term[1:]
                exp = parse_exp(term)

        parsed[exp] = parsed.get(exp, 0.0) + mul
        i = end

    return parsed


def parse(equation: str) -> Dict[int, float]:
    equation = ''.join(c for c in equation if not c.isspace()).upper()

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
        if parsed[exp] == 0.0:
            del parsed[exp]

    return parsed


def main() -> None:
    # Parser tests
    tests = [
        ("1 + 2 + 3", {0: 6}),
        ("1 + 2 + 3 * X^0", {0: 6}),
        ("1 + 2 + 3 * X", {0: 3, 1: 3}),
        ("1 + 2 * X ^ 1 + 3 * X", {0: 1, 1: 5}),
        ("1 + 2 * X ^ 1 + 3 * X - 3 * X ^ 0", {0: -2, 1: 5}),
        ("1 + 2 * X ^ 1 + 3 * X - 7 * X ^ 2", {0: 1, 1: 5, 2: -7}),
        ("-5 * X + 1 + 2 * X ^ 1 + 3 * X - 7 * X ^ 2", {0: 1, 1: 0, 2: -7}),
        ("-5 * X ^ 8 + 1 + 2 * X ^ 1 + 3 * X - 7 * X ^ 2", {0: 1, 1: 5, 2: -7, 8: -5}),
    ]

    for eq, p in tests:
        res = parse(eq)
        if res != p:
            print("Failed for", eq)
            print("Found:", res)
            print("Expected:", p)
            print()


if __name__ == "__main__":
    main()
