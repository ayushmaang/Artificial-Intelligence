import numpy
class Percept():
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold
        self.inputs = None

    def set_inputs(self, inputs):
        self.inputs = inputs

    def activiator(self, sum):
        if sum > self.threshold:
            return 1
        else:
            return 0

    def multiply(self):
        sum = 0
        for i in range(len(self.inputs)):
            sum+= self.inputs[i].input*self.weights[i]
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

        sum = numpy.dot(self.inputs,self.weights)
        if sum >= self.threshold:
            return 1
        else:
            return 0

class Input:
    def __init__(self):
        self.input = None
    def set_value(self,input):
        self.input = input

x1 = Input()
x2 = Input()
node_3 = Percept([1,1],1.5)
node_4 = Percept([1,1],.5)
node_5 = Percept([-2,1],.5)
node_3.set_inputs([x1,x2])
node_4.set_inputs([x1,x2])
node_5.set_inputs([node_3, node_4])
xor = node_5

xnor = "1001"

for a in range(2):
    for b in range(2):
        x1.set_value(a)
        x2.set_value(b)
        print(a,b,xor.eval())
