# create function that convert python given expression to latex string
def to_latex(expr):
    return expr.latex()

a = 2
b =3
to_latex(a**2+b)