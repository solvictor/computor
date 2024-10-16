from typing import Dict, Tuple


VALID_CHARS = "0123456789X=.-+*^"


def next_index(string: str, charset: str, start: int = 0) -> int:
    """Function that return the first index of any character in charset

    Args:
        string (str): string to search in
        charset (str): charset to search
        start (int, optional): starting index. Defaults to 0.

    Returns:
        int: index of the first character in both string and charset or -1
    """

    for i in range(start, len(string)):
        if string[i] in charset:
            return i
    return -1


def parse_exp(string: str) -> int:
    """Parse an exponent

    Args:
        string (str): the string

    Raises:
        SyntaxError: if the exponent is not well formatted

    Returns:
        int: the exponent
    """

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


def parse_term(polynom: str, i: int) -> Tuple[int, int, int]:
    """Parse the term at index i in polynom

    Args:
        polynom (str): the polynom
        i (int): starting index of the term

    Raises:
        SyntaxError: if the term is not well formatted

    Returns:
        Tuple[int, int, int]: exponent, multiplier, end index
    """

    end = next_index(polynom, "+-", i + 1)
    if end == -1:
        end = len(polynom)

    term = polynom[i:end]
    mul = 1.0
    exp = 0

    # TODO Better parsing
    # part = term.split("*")
    # for e in part:
    #     try:
    #         mul *= float(e)
    #     except Exception:
    #         if e[0] == '-':
    #             mul *= -1.0
    #         if e[0] in "+-":
    #             e = e[1:]
    #         exp += parse_exp(e)

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
    return exp, mul, end


def parse_poly(polynom: str) -> Dict[int, float]:
    """Parse a polynom

    Args:
        polynom (str): the polynom

    Raises:
        SyntaxError: if the polynom is not well formatted

    Returns:
        Dict[int, float]: exponent: mulitplier for each term
    """

    if not polynom:
        raise SyntaxError("Invalid equation: polynom is empty")

    if not all(c in VALID_CHARS for c in polynom):
        raise SyntaxError("Invalid equation: bad characters found")

    parsed = {}  # exp: mul

    i = 0
    while i < len(polynom):
        exp, mul, end = parse_term(polynom, i)
        parsed[exp] = parsed.get(exp, 0.0) + mul
        i = end

    return parsed


def parse(equation: str) -> Dict[int, float]:
    """Parse an equation

    Args:
        equation (str): the equation

    Raises:
        SyntaxError: if the equation is not well formated

    Returns:
        Dict[int, float]: exponent: mulitplier for each term
    """

    equation = ''.join(c for c in equation if not c.isspace()).upper()

    if not equation:
        raise SyntaxError("Invalid equation: equation is empty")

    equals = equation.count("=")
    if equals > 1:
        raise SyntaxError("Invalid equation: more than one '=' found")
    elif equals == 0:  # May be considered invalid too
        equation += "=0"

    left, right = equation.split("=")
    parsed = parse_poly(left)

    for exp, mul in parse_poly(right).items():
        parsed[exp] = parsed.get(exp, 0.0) - mul

    return {k: v for k, v in parsed.items() if v != 0.0}


def main() -> None:
    """Tests the parser"""

    # Parser tests
    tests = [
        ("1 + 2 + 3", {0: 6}),
        ("1 + 2 + 3 * X^0", {0: 6}),
        ("1 + 2 + 3 * X", {0: 3, 1: 3}),
        ("1 + 2 * X ^ 1 + 3 * X", {0: 1, 1: 5}),
        ("1 + 2 * X ^ 1 + 3 * X - 3 * X ^ 0", {0: -2, 1: 5}),
        ("1 + 2 * X ^ 1 + 3 * X - 7 * X ^ 2", {0: 1, 1: 5, 2: -7}),
        ("-5 * X + 1 + 2 * X ^ 1 + 3 * X - 7 * X ^ 2", {0: 1, 2: -7}),
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
