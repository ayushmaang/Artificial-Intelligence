import random

def f (x):
    return (x-3)**2 + 2

def minimization(a, b, e):
    # Optimal is golden ratio for c and
    # Easy way to pick c and d is to use 3rds
    # Pick c, d e[a, b]
    # golden = (1+5**0.5)/2
    while b - a > e:
        boom = abs(b - a) / 3
        c = a + boom
        d = c + boom
        # print(b-a)
        if f(c) < f(d):
            a,b = a,d
        else:
            a,b = c,b
    return a

print(minimization(0,6,.000001))
