import sympy as sp

x = sp.symbols('x')

f = x**3 + x**2 + 3
d = sp.diff(f, x)


y = float(d.subs({x:5}))
print(type(y))