from fractions import Fraction
from numbers import Number


def __format(x: float, add_plus: bool = False) -> str:
    """Format a float

    Args:
        x (float): float to format
        add_plus (bool, optional): add + sign if x >= 0. Defaults to False.

    Returns:
        str: formatted float
    """

    d = str(x)
    f = str(Fraction(d).limit_denominator())
    best = min(f, d, key=len)
    if add_plus and x >= 0:
        best = '+' + best
    return best.removesuffix(".0")


def format_sol(n: Number) -> str:
    """Format a solution number

    Args:
        n (Number): number to format

    Returns:
        str: formatted solution
    """

    if n == 0.0:
        return "0"

    if isinstance(n, complex):
        real, imag = n.real, n.imag
        if real:
            fimag = __format(imag, True)
            if abs(imag) == 1:
                fimag = fimag.replace('1', '')
            res = f"{__format(real)} {fimag}i"
        else:
            res = f"{__format(imag)}i"
            if abs(imag) == 1:
                res = res.replace('1', '')
    else:
        res = __format(n)

    return res
