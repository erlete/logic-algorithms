from main import *

# Result display function:

def summary(*statements):
    t1, t2, t3 = 'ID:', 'Value:', 'Element:'
    idlen, vallen, ellen = 5, 15, 60
    title = t1 + (idlen - len(t1)) * ' ' + t2 + (vallen - len(t2)) * ' ' + t3 + (ellen - len(t3)) * ' '
    print('-' * 80)
    print(title)
    print('-' * 80)
    for index in range(len(statements)):
        r1 = str(index)
        r2 = str(statements[index].getValue())
        r3 = str(statements[index])
        row = r1 + (idlen - len(r1)) * ' ' + r2 + (vallen - len(r2)) * ' ' + r3 + (ellen - len(r3)) * ' '
        print(row)

# Test area:

switch = True

# Test 1: Normal demonstration

p = Proposition('rains')
q = Proposition('home')
r = Proposition('cafe')

s1 = Symbol(p, verbose = switch)
s2 = Not(q, verbose = switch)
s3 = Implicative(p, Or(q, r, verbose = switch), verbose = switch)

summary(p, q, r, s1, s2, s3)

# Test 2: Incoherence Error

p = Proposition('rains')
q = Proposition('coat')
r = Proposition('umbrella')

s1 = Symbol(p, verbose = switch)
s2 = Not(q, verbose = switch)
s3 = Implicative(p, And(q, r, verbose = switch))

summary(p, q, r, s1, s2, s3)

# Test 3: Overall demonstration

p = Proposition('p')
q = Proposition('q')

s1 = Symbol(p, verbose = switch)
s2 = Not(q, verbose = switch)
s3 = And(p, q, verbose = switch)
s4 = Or(p, q, verbose = switch)
s5 = Implicative(p, q, verbose = switch)
s6 = BiImplicative(p, q, verbose = switch)

summary(p, q, s1, s2, s3, s4, s5, s6)
