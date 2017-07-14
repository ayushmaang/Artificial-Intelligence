import math
import random
import numpy

class Percept():
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold
        self.inputs = None
        self.constant=4.2

    def set_inputs(self, inputs):
        self.inputs = inputs
    def set_constant(self,constant):
        self.constant = constant

    def activiator(self, sum):
        sum -= self.threshold
        res = 1 / (1 + math.e ** (-self.constant * sum))
        return res

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
                # print(actual_inputs)
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
x1 = Input()
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



def accuracy(constant):
    count = 0
    node_3.set_constant(constant)
    node_4.set_constant(constant)
    node_5.set_constant(constant)
    node_6.set_constant(constant)
    node_7.set_constant(constant)
    node_8.set_constant(constant)
    for i in range(500):
        num = (numpy.random.normal(0.5,0.5))
        num1 = (numpy.random.normal(0.5,0.5))
        a = (random.random() * 3) -1.5
        b = (random.random() * 3) -1.5
        #num = a
        #num1 = b
        # print(num1,num)
        x1.set_value(num)
        y1.set_value(num1)
        # print(num,num1)
        answer = (num**2) + (num1**2) < 1
        res = round(andnode.eval())
        # print(res)
        if answer == False and res == 0:
            count += 1
        elif answer == True and res == 1:
            count += 1
    return (count/500)*100


def err(w):
    answers = numpy.array([0, 1, 1, 0])
    error = 0
    x1 = Input()
    x2 = Input()
    # node_3 = Percept([1, 1], 1.5)
    # node_4 = Percept([1, 1], .5)
    # node_5 = Percept([-2, 1], .5)
    node_3 = Percept([w[0], w[1]], -w[2])
    node_4 = Percept([w[3], w[4]], -w[5])
    node_5 = Percept([w[6], w[7]], -w[8])
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
    while err(w) > 0.1:
        count += 1
        if count == 3000:
            count = 0
            w = numpy.array([random.uniform(-1, 1) for i in range(9)])
        delta = [random.uniform(-learnRate, learnRate) for i in range(9)]
        if err(w + delta) < err(w):
            w = w + delta

    for i in range(len(w)):
        w[i] = round(w[i])

    return w, count, err(w)

def kclimb(learnRate):
    w = 4.2
    num = 0
    acc = accuracy(w)
    while acc < 99:
        print(w)
        num += 1
        if num == 100:
            count = 0
        delta = random.uniform(-learnRate, learnRate)
        if accuracy(w + delta) < acc:
            w = w + delta
        print(accuracy(w))
    return w, num, accuracy(w)


print (hillclimb(.1))
# answer = (kclimb(.1))
# print(accuracy(answer[2]))
# print(accuracy(4.2))
