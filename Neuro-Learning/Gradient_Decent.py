import numpy as np
import random
import math
import matplotlib.pyplot as plt

def f(vector):
    x = vector[0]
    y = vector[1]
    # return 4 * x**2 - 3 * x * y + 2 * y**2+ 24*x - 20*y
    return (1-y)**2 + 100*(x-y**2)**2

def minimization(f, a, b, e):
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
            a, b = a, d
        else:
            a, b = c, b
    return a


def gradient_f(vector):
    x = vector[0]
    y = vector[1]
    return np.array([200*x - 200*y**2, -400*y*(x-y**2) + 2*y - 2])

    # return np.array([(8 * x) - (3 * y) + 24, -(3 * x) + (4 * y) - 20])


def err(vector):
    return vector[0] ** 2 + vector[1] ** 2

##################################
##     Step 4 with dynamic λ    ##

def gradient_descent_4(learning_rate):
    # x = np.array([random.uniform(-10, 10), random.uniform(-10, 10)])
    x = np.array([0,0])
    count = 0
    λ_min = minimization(lambda λ: f(x - λ*gradient_f(x)), 0, 1, 0.001)
    while err(gradient_f(x)) > .00000000:
        count += 1
        λ_min = minimization(lambda λ: f(x - λ * gradient_f(x)), 0, 1, 0.001)
        # print(count)
        print(x, err(x))
        x = x - λ_min * gradient_f(x)
    print(count)
    return x, err(x)

##################################
##################################
##     Step 3 with graph λ    ##
# def gradient_descent(learning_rate):
#     x = np.array([random.uniform(-10, 10), random.uniform(-10, 10)])
#     count = 0
#     # λ_min = min_λ(f(x - λ * gradient_f(x))
#     # λ_min = minimization(lambda λ: f(x - λ*f(x)), 0, 1, 0.001)
#     while err(gradient_f(x)) > .1:
#         count += 1
#         # print(count)
#         # print(x, err(gradient_f(x)))
#         x = x - learning_rate * gradient_f(x)
#
#     return count
#
# print(gradient_descent(0.1))
# arrayx = []
# arrayy = []
# for i in range(1,100,1):
#     learning = i/5000
#     arrayy.append(gradient_descent(learning))
#     arrayx.append(learning)
#
# plt.plot(arrayx, arrayy)
# plt.show()
##################################

print(gradient_descent_4(0.1))

