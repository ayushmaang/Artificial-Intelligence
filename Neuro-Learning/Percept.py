import numpy
import math
import random

count = 0
learnRate = 1

def solutionFound(accuracy):
    if accuracy > .99:
        return True
    return False


def opposite(t):
    return 1 / (1 + math.e ** (-40*t))

def train(training_set):
    w = random.choice(training_set)
    w = w[0]
    for i in range(100):
        for vector in training_set:
            f = opposite(numpy.dot(vector[0], w))
            w = w + learnRate*(vector[1] - f)*vector[0]

    accuracy = 1
    acc_sum = 0
    for vector in training_set:
        temp = numpy.dot(vector[0],w)
        acc_sum += abs(vector[1] - opposite(temp))

    accuracy-=acc_sum/len(training_set)

    return (w, accuracy)



def run(n):
    n = 2**n
    count = 0
    correct = 0
    correctArray = []
    for i in range(2**n):
        # print (i)
        string = bin(i)[2:]
        for j in range(n-len(bin(i)[2:])):
            string = '0' + string
        # print (string)
        training_set = []
        for j in range(n):
            newbin = bin(j)[2:]
            for k in range(int(math.log2(n) - len(bin(j)[2:]))):
                newbin = '0' + newbin
            temparray = []
            for i in range(len(newbin)):
                temparray.append(int(newbin[i]))
            temparray.append(1)
            training_set.append((numpy.array(temparray),int(string[j])))

        array = (train(training_set))
        # print(array[0])
        count+=1

        if(round(array[1]) == 1):
            correct+=1
            correctArray.append(array[0])

    # print(str(correct),"/",str(count))
    return correctArray

cool = run(2)

print(len(cool))