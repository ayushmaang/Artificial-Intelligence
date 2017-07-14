import random
import numpy
import math
import matplotlib.pyplot as plt

import random
import math
import csv
import matplotlib.pyplot as plt
from collections import deque

global columnToIndex
global treeSize
treeSize = 0
class Edge:
    def __init__(self, s, e, atr):
        global treeSize
        treeSize += 1
        self.startNode = s
        self.endNode = e
        self.attribute = atr

    def __str__(self):
        return self.attribute

class Percept():
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold
        self.inputs = None

    def set_inputs(self, inputs):
        self.inputs = inputs

    def activiator(self, sum):
        sum -=self.threshold

        res = 1/(1+math.e**(-40*sum))
        return res
        # if res > .5:
        #     return 1
        # else:
        #     return 0
        # sum -=self.threshold


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


class Node:

    def __init__(self, question, answer, par, freq):
        self.question = question
        self.answer = answer
        self.parent = par
        self.pruned = False
        self.freq = freq
        self.edges = dict()

    def __str__(self):
        return "" + self.question + " " + self.answer

    def addEdge(self, atr, nextNode):
        edge = Edge(self, nextNode, atr)
        self.edges[atr] = edge

    def traverseTree(self, testCase): #testCase is type string
        global columnToIndex
        #print(self.question)
        indexToLookAt = columnToIndex[self.question]
        # print (indexToLookAt)
        # print (testCase)
        value = testCase[indexToLookAt]
        if value == "?":
            rep, dem = self.dfs()
            if rep is None and dem is None:
                return "Idk"
            if rep > dem:
                #print ("did something")
                return "republican"
            else:
                #print ("did something d")
                return "democrat"
        '''if value == "?":
            return "werewlrjerj"'''
        currentEdge = self.edges[value]
        nextNode = currentEdge.endNode
        if nextNode.answer is not None:
            return nextNode.answer
        return nextNode.traverseTree(testCase)

    def dfs(self):
        try:
            demCount = 0
            repCount = 0
            if self.answer is not None:
                if self.answer == "democrat":
                    demCount += self.freq
                else:
                    repCount += self.freq
                return repCount, demCount
            else:
                for edge in self.edges:
                    rep, dem = self.edges[edge].endNode.dfs()
                    demCount += dem
                    repCount += rep
            return repCount, demCount
        except:
            return None, None

CLASS_idx = 0 # index of the answer column after reading CSV file

def get_data(file, start, finish):
    global CLASS_idx
    rows = set()
    with open(file) as csvfile:
        """ Read data in from a csv file
            stores the index of the classification column
            in a global variable
        """
        reader = csv.reader(csvfile)
        headers = next(reader)[1:]
        global columnToIndex
        columnToIndex = dict()
        for i in range(len(headers)):
            columnToIndex[headers[i]] = i-1
        array = [row for row in reader]
        random.shuffle(array)
        # print (len(array))
        ds = dict()
        count = start


        indexes = set()

        for i in range(finish-start):
                row = array[i]
                rows.add(row[0])  # take the P out
                ds[row[0]] = row[1:]


        csvfile.close()
    CLASS_idx = len(headers) - 1
    return ds, headers

def answer(file):
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)[1:]
        ds = [row[11] for row in reader]

    return ds

def test_data(headNode, file, start,finish):
    global CLASS_idx
    with open(file) as csvfile:
        """ Read data in from a csv file
            stores the index of the classification column
            in a global variable
        """
        reader = csv.reader(csvfile)
        headers = next(reader)
        global columnToIndex
        columnToIndex = dict()
        for i in range(len(headers)):
            columnToIndex[headers[i]] = i-1
        ds=dict()
        for row in range(finish-start):
            row = next(reader)
            ds[row[0]] = row[1:]
        csvfile.close()
    CLASS_idx = len(headers) - 1
    testList = dict()
    for key in ds:
        temp = ds[key]
        temp = temp[:len(temp)-1]
        testList[key] = temp

    count = 0
    answers = dict()
    for key in testList:
        testCase = testList[key]
        newKey = int(key[1:]) - 1
        answers[newKey] = headNode.traverseTree(testCase)
    #print ("answers length: " + str(len(answers)))
    return answers


def rand_dataset(r,c):
    """ create a random binary dataset of size r x c
    """
    return {i: [random.randrange(2) for i in range(c)] for i in range(r)}

def val_list(data, column):
    """ return a list of all values contained in the domain
        of the parameter 'column'
    """
    return [val[column] for val in data.values()]

def val_set(data, column):
    """ return the set of all values contained in the domain
        of the parameter 'column'
    """
    return set(val_list(data, column))

def restrict(data, column, value): # aka extract
    """ return a dictionary corresponding to the rows in
        data in which parameter 'column' == value
    """
    return {a:data[a] for a in data if data[a][column]==value}

def freq_dist(data_dict):
    """ returns a dict where the keys are unique
        elements in the final column and the values are the
        frequency counts of those elements in data_dict.
    """
    vals = val_list(data_dict, CLASS_idx)
    return {a: vals.count(a) for a in set(vals)}

def freq_entropy(freq_dict):
    """ returns the entropy of the frequency distribution
        passed in as a dict: {(x = freq(x))}
    """
    f = list(freq_dict.values())
    s = sum(f)
    p = [i / s for i in f]
    return (-sum([i * math.log(i, 2) for i in p if i > 0]))

def parameter_entropy(data, col):
    """ returns the average entropy associated
        with the parameter in column 'col'
        in the dictionary 'data'
    """
    length = len(data)
    total = 0
    for v in val_set(data, col):
        ds = restrict(data, col, v)
        l = len(ds)
        e = freq_entropy(freq_dist(ds))
        total += l / length * e
    return total

def make_tree(ds, level, parents):
    initial_h = freq_entropy(freq_dist(ds))
    best = max((initial_h - parameter_entropy(ds, i), i) for i in range(CLASS_idx))
    p = best[1]
    # print("---" * level, headers[p], "(initial = %3.3f, gain=%3.3f)"%(initial_h, best[0]), "?")
    # print("---" * level, headers[p], "?")
    currentNode = Node(headers[p], None,None, 0)
    for v in val_set(ds, p):
        if v == "?":
            continue
        new_ds = restrict(ds, p, v)
        freqs = freq_dist(new_ds)
        if freq_entropy(freqs) < .001:
            # print("---" * level + ">", headers[p], "=", v, freqs)
            # print("---" * level + ">", v, freqs)
            # print (list(freq.keys()))[0]
            valAndFreq = findMost(freqs)
            currentNode.addEdge(v, Node(None, valAndFreq[0], currentNode, valAndFreq[1]))
        else:
            # print("---" * level + ">", headers[p], "=", v, "...", freqs)
            # print("---" * level + ">", v, freqs)
            nextNode = make_tree(new_ds, level + 1, parents + [p])
            currentNode.addEdge(v, nextNode)
    return currentNode

def findMost(freqs):
    currentMax = 0
    val = None
    for key in freqs:
        if freqs[key] > currentMax:
            currentMax = freqs[key]
            val = key
    return val, currentMax

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


def test(testCases, weights):
    correct = 0
    for testCase in testCases:
        sum = 0
        for i in range(len(weights)):
            jaunt = testCase[0][i]
            weight = weights[i]
            sum += jaunt*weight
        res = opposite(sum)
        if res == testCase[1]:
            correct += 1
    return correct

def majority(newbin):
    oneCount = 0
    for char in newbin:
        if char == '1':
            oneCount += 1
    if oneCount >= 5:
        return 1
    else:
        return 0

def createTrainingSet(n):
    training_set = []
    for i in range(n):
        val = random.randint(0, 2**10-1)
        newbin = bin(val)[2:]
        initialLen = len(newbin)
        for k in range(10 - initialLen):
            newbin = '0' + newbin
        temparray = []
        for i in range(len(newbin)):
            temparray.append(int(newbin[i]))
        temparray.append(1)

        num = majority(newbin)
        training_set.append((numpy.array(temparray), num))
    # print (len(training_set))
    return training_set

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
            # print (newbin)
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
            if correct == 200:
                break
    print(str(correct),"/",str(count))
    return correctArray

cool = run(2)
print((cool))
x1 = Input()
x2 = Input()
tool = 0
xors = []
solution = 0
for i in range(len(cool)):
    node_3 = Percept([cool[i][0], cool[i][1]], -cool[i][2])
    for j in range(len(cool)):
        node_4 = Percept([cool[j][0], cool[j][1]], -cool[j][2])
        for k in range(len(cool)):
            node_5 = Percept([cool[k][0], cool[k][1]], -cool[k][2])
            node_3.set_inputs([x1, x2])
            node_4.set_inputs([x1, x2])
            node_5.set_inputs([node_3, node_4])
            xor = node_5
            total = ""
            for a in range(2):
                for b in range(2):
                    x1.set_value(a)
                    x2.set_value(b)
                    bice = xor.eval()
                    bice = int(round(bice))

                    total += str(bice)
            # print(total)
            if total == "0110":
                print(solution)
                solution+=1
                print("node_3 weights",[cool[i][0], cool[i][1]], -cool[i][2])
                print("node_4 weights",[cool[j][0], cool[j][1]], -cool[j][2])
                print("node_5 weights",[cool[k][0], cool[k][1]], -cool[k][2])
                print("Solution:",i,j,k,"\n")
                tool+=1

print(tool)

# arrayx = []
# arrayy = []
# decisionx = []
# decisiony = []
# for i in range(10,100,1):
#     arrayx.append(i)
#     trainArray = createTrainingSet(i)
#     weights = train(trainArray)[0]
#     # print (weights)
#     testArray = createTrainingSet(100)
#     accuracy = (test(testArray,weights))
#     arrayy.append(accuracy)
#
#     DS, headers = get_data("train.csv", 0, i)
#     actualData = answer("test.csv")
#     headNode = make_tree(DS, 1, [0])
#     queue = deque()
#     queue.append(headNode)
#     correct = 0
#     answers = test_data(headNode, "test.csv", 0, 100)
#     skipped = 0
#     for x in range(0, len(answers)):
#         temp = actualData[x]
#         temp2 = answers[x]
#         if actualData[x] == answers[x]:
#             correct += 1
#     decisionx.append(i)
#     decisiony.append(correct)
#
#
# plt.plot(arrayx,arrayy)
# plt.plot(decisionx, decisiony)
# plt.show()
