import math
import random
import numpy
import matplotlib.pyplot as plt

class Percept():
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold
        self.inputs = None

    def set_inputs(self, inputs):
        self.inputs = inputs

    def activiator(self, sum):
        sum -= self.threshold
        res = 1 / (1 + math.e ** (-4.2 * sum))
        return res
        # if sum > self.threshold:
        #     return 1
        # else:
        #     return 0



    def multiply(self):
        sum = 0
        for i in range(len(self.inputs)):
            sum+= self.inputs[i]. input*self.weights[i]
        return sum

    def eval(self):
        for i in range(len(self.inputs)):
            cool = type(self.inputs[i]).__name__
            if cool is "Percept":
                actual_inputs = []
                for j in self.inputs:
                    actual_inputs.append(j.eval())
                num = numpy.dot(actual_inputs,self.weights)
                return self.activiator(num)
            else:
                sum = self.multiply()
                return self.activiator(sum)


    def __str__(self):
        return self.weights, self.inputs

class Input:
    def __init__(self):
        self.input = None
    def set_value(self,input):
        self.input = input
    def __str__(self):
        return self.input
'''x1 = Input()
node_3 = Percept([-1],-1)
node_4 = Percept([1],-1)
node_5 = Percept([1,1],1.5)
node_3.set_inputs([x1])
node_4.set_inputs([x1])

node_6 = Percept([-1],-1)
node_7 = Percept([1],-1)
node_8 = Percept([1,1],1.5)


node_5.set_inputs([node_3, node_4])
node_8.set_inputs([node_6, node_7])
y1 = Input()
node_6.set_inputs([y1])
node_7.set_inputs([y1])
x1.set_value(.75)
y1.set_value(1.75)
andnode = Percept([1.05,1.05], 1.5)
andnode.set_inputs([node_5, node_8])

count = 0
for i in range(1000):
    a = (random.random() * 3) - 1.5
    b = (random.random() * 3) - 1.5

    x1.set_value(a)
    y1.set_value(b)

    answer = (a**2) + (b**2) < 1
    res = round(andnode.eval())
    # print(res)
    if answer == False and res == 0:
        count += 1
    elif answer == True and res == 1:
        count += 1
print ((count/1000)*100)'''


def err(w):
    answers = numpy.array([0, 1, 1, 0])
    error = 0
    x1 = Input()
    x2 = Input()
    # node_3 = Percept([w[0], w[1]], -w[2])
    # node_4 = Percept([w[3], w[4]], -w[5])
    # node_5 = Percept([w[6], w[7]], -w[8])
    # node_3.set_inputs([x1, x2])
    # node_4.set_inputs([x1, x2])
    # node_5.set_inputs([node_3, node_4])

    x1 = Input()
    x2 = Input()
    node_3 = Percept([1, 1], 1.5)
    node_4 = Percept([1, 1], .5)
    node_5 = Percept([-2, 1], .5)
    node_3.set_inputs([x1, x2])
    node_4.set_inputs([x1, x2])
    node_5.set_inputs([node_3, node_4])



    results = []
    for i in range(2):
        for j in range(2):
            x1.set_value(i)
            x2.set_value(j)
            f = node_5.eval()
            results.append(f)
    for i in range(len(results)):
        error += abs(results[i] - answers[i])
    return error


def hillclimb(learnRate):
    count = 0
    w = numpy.array([random.uniform(-1, 1) for i in range(9)])

    while err(w) > 0.01:
        count += 1
        if count == 600:
            count = 0
            w = numpy.array([random.uniform(-1, 1) for i in range(9)])
        delta = [random.uniform(-learnRate, learnRate) for i in range(9)]
        if err(w + delta) < err(w):
            w = w + delta
    return w, count, err(w)

hillclimb(.1)

# lr = .1
# arrayx = []
# arrayy = []
# while(lr < 2):
#     print (lr)
#     tot = 0
#     for i in range(10):
#         print (i)
#         tot += hillclimb(lr)[1]
#     tot /= 10
#     arrayx.append(lr)
#     arrayy.append(tot)
#     lr += .05
# plt.plot(arrayx, arrayy)
# plt.show()
