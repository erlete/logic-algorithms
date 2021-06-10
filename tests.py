from main import *

# Result display function:

def summary(*statements, info: str = ''):
    title = ' Results: ' if info == '' else f" Results ({info}): "
    print(f"{'+' * 80}\n{title.center(80)}\n{'+' * 80}")
    for element in statements:
        print(f"Value: {(str(element.getSelfValue()) + ' ').ljust(12, '-')} " + f"for element {element}")
    print(f"{'+' * 80}\n")

# Test area:

switch = True

# Test 1: Normal demonstration

p = Proposition('rains')
q = Proposition('home')
r = Proposition('cafe')

s1 = Yes(p, verbose = switch)
s2 = Not(q, verbose = switch)
s3 = Implicative(p, Or(q, r, verbose = switch), verbose = switch)

summary(p, q, r, s1, s2, s3, info = 'test 1')

# Test 2: Incoherence Warning

p = Proposition('rains')
q = Proposition('coat')
r = Proposition('umbrella')

s1 = Yes(p, verbose = switch)
s2 = Not(q, verbose = switch)
s3 = Implicative(p, And(q, r, verbose = switch))

summary(p, q, r, s1, s2, s3, info = 'test 2')

# Test 3: Overall demonstration

p = Proposition('p')
q = Proposition('q')

s1 = Yes(p, verbose = switch)
s2 = Not(q, verbose = switch)
s3 = And(p, q, verbose = switch)
s4 = Or(p, q, verbose = switch)
s5 = Implicative(p, q, verbose = switch)
s6 = BiImplicative(p, q, verbose = switch)

summary(p, q, s1, s2, s3, s4, s5, s6, info = 'test 3')

# Test 4: XOr vs Or testing

p = Proposition('p')
q = Proposition('q')
r = Proposition('r')

s1 = Yes(p)
s2 = Not(q)
s3 = Yes(r)
s4 = Or(p, q)
s5 = XOr(p, q)
s6 = Or(p, r)
s7 = XOr(p, r)

summary(p, q, s1, s2, s3, s4, s5, s6, s7, info = 'test 4')
