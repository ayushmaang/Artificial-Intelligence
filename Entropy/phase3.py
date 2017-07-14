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
            columnToIndex[headers[i]] = i
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
    return ds, headers, rows

def answer(file):
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)[1:]
        ds = [row[17] for row in reader]

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
        if key in rows:
            continue
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
        if freq_entropy(freqs) < 1/4:
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
arrayx = []
arrayy = []
sizex = []
sizey = []
count = 0

def pruneTree(queue, headNode):
    for node in queue:
        originalPruned = False
        originalAnswer = None
        if node.pruned == True:
            originalPruned = True
        if node.answer is not None:
            originalAnswer = node.answer
        node.pruned = True
        repCount, demCount = node.dfs()
        if repCount > demCount:
            node.answer = "republican"
        else:
            node.answer = "democrat"
        if repCount > (8*demCount) or demCount > (8*repCount):
            node.edges = None
            continue
        else:
            node.answer = originalAnswer
            node.pruned = originalPruned

def bfs(queue):
    finalQueue = deque()
    while True:
        try:
            nextNode = queue.popleft()
            finalQueue.append(nextNode)
            if nextNode.answer is not None:
                continue
            for edge in nextNode.edges:
                queue.append(nextNode.edges[edge].endNode)
        except:
            break
    return finalQueue

for i in range(10,201,1):
    averageCount = 0
    average = 0
    for j in range(10):

        if i == 200:
            afpiaejf = "hi"
        DS, headers, rows = get_data("newfile.csv",0,i)
        actualData = answer("house-votes-84.csv")
        headNode = make_tree(DS, 1, [0])
        queue = deque()
        queue.append(headNode)
        # finalQueue = bfs(queue)
        # treeSizeBefore = len(finalQueue)
        # pruneTree(finalQueue, headNode)
        global treeSize
        sizex.append(i)
        # testLength = deque()
        # testLength.append(headNode)
        # treeSizeAfter = len(bfs(testLength))
        # sizey.append(treeSizeAfter)
        treeSize = 0
        correct = 0
        answers = test_data(headNode, "house-votes-84.csv", 0, 435)
        skipped = 0

        for x in range(0, len(answers)):
            if "P" + str(x+1) in rows:
                skipped += 1
                continue
            temp = actualData[x]
            temp2 = answers[x]
            if actualData[x] == answers[x]:
                correct += 1

        total = len(answers) - skipped
        current = (correct/total)
        average += current
        averageCount+=1
        #print (str(averageCount) + " " + str(average))
    average/=10

    arrayy.append(average*100)
    arrayx.append(i)

plt.plot(sizex, sizey)
plt.plot(arrayx,arrayy)
plt.show()
