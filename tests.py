from main import *

def test1(switch = False): # Valid demonstration
    p = Proposition('rains')
    q = Proposition('home')
    r = Proposition('cafe')

    s1 = Symbol(p, verbose = switch)
    s2 = Not(q, verbose = switch)
    s3 = Implicative(p, Or(q, r, verbose = switch), verbose = switch)

    summary(p, q, r, s1, s2, s3)

def test2(switch = False): # IncoherenceError demonstration:
    p = Proposition('rains')
    q = Proposition('coat')
    r = Proposition('umbrella')

    s1 = Symbol(p, verbose = switch)
    s2 = Not(q, verbose = switch)
    s3 = Implicative(p, And(q, r, verbose = switch))

    summary(p, q, r, s1, s2, s3)

test1(True)
test2(True)
