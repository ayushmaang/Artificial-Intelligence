import random
import math
import csv
import matplotlib.pyplot as plt

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

class Node:

    def __init__(self, question, answer, par):
        self.question = question
        self.answer = answer
        self.parent = par
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
        value = testCase[indexToLookAt]
        if value == "?":

            return "ERROR"

            rep, dem = self.dfs()
            if rep is None and dem is None:
                return "Idk"
            if rep > dem:
                # print ("did something")
                return "False"
            else:
                # print ("did something d")
                return "True"

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
                if self.answer == "True":
                    demCount += 1
                else:
                    repCount += 1
            for edge in self.edges:
                rep, dem = self.edges[edge].endNode.dfs()
                demCount += dem
                repCount += rep
            return repCount, demCount
        except:
            return None, None

CLASS_idx = 0 # index of the answer column after reading CSV file


def get_data(file):
    global CLASS_idx
    with open(file) as csvfile:
        """ Read data in from a csv file
            stores the index of the classification column
            in a global variable
        """
        reader = csv.reader(csvfile)
        headers = next(reader)[1:]
        ds = {row[0]: row[1:] for row in reader}
        csvfile.close()
    CLASS_idx = len(headers) - 1
    return ds, headers

def answer(file):
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)[1:]
        ds = [row[21] for row in reader]

    return ds

def test_data(headNode, file, start,finish):
    global CLASS_idx
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
            columnToIndex[headers[i]] = i
        for i in range(start):
            next(reader)
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
        newKey = int(key)
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
    print("---" * level, headers[p], "(initial = %3.3f, gain=%3.3f)"%(initial_h, best[0]), "?")
    print("---" * level, headers[p], "?")
    currentNode = Node(headers[p], None,None)
    for v in val_set(ds, p):
        if v == "?":
            continue
        new_ds = restrict(ds, p, v)
        freqs = freq_dist(new_ds)
        if freq_entropy(freqs) < 0.001:
            print("---" * level + ">", headers[p], "=", v, freqs)
            print("---" * level + ">", v, freqs)
            # print (list(freq.keys()))[0]
            currentNode.addEdge(v, Node(None, list(freqs.keys())[0], currentNode))
        else:
            print("---" * level + ">", headers[p], "=", v, "...", freqs)
            print("---" * level + ">", v, freqs)
            global leavesCount
            leavesCount +=1
            nextNode = make_tree(new_ds, level + 1, parents + [p])
            currentNode.addEdge(v, nextNode)
    return currentNode

arrayx = []
arrayy = []
sizex = []
sizey = []
count = 0



DS, headers = get_data("quizC_train.csv")
global leavesCount
leavesCount = 0
actualData = answer("quizC_test_b.csv")
headNode = make_tree(DS, 1, [0])
global treeSize
treeSize = 0
correct = 0
answers = test_data(headNode, "quizC_test_b.csv", 0, 1000)


for i in range(999):
    test = actualData[i]
    temp = answers[i]
    if actualData[i] == answers[i]:
        correct+=1


# print(treeSize)
print(answers)
print(len(actualData))
print(correct)
# print(leavesCount)

