import random
import math
import csv
from copy import deepcopy
import matplotlib.pyplot as plt

def get_data_training(file):
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
        ds = {row[0]: row[1:] for row in reader}
        dscopy = deepcopy(ds)
        for row in ds:
            if "?" in dscopy[row]:
                dscopy.pop(row)
            else:
                print ("? was not in " + str(dscopy[row]))
        ds = dscopy
        csvfile.close()
    CLASS_idx = len(headers) - 1
    return ds, headers

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
    file = open("test.csv", 'w')
    training_set = []
    for i in range(n):
        val = random.randint(0, 2**10)
        newbin = bin(val)[2:]
        initialLen = len(newbin)
        for k in range(10 - initialLen):
            newbin = '0' + newbin
        for i in range(len(newbin)):
            training_set.append(int(newbin[i]))
            file.write(newbin[i] + ",")
        num = majority(newbin)
        file.write(str(num) + "\n")
    # print (len(training_set))
    return training_set

# DS, headers = get_data_training("quizC_test_b.csv")
file = open("train.csv", 'w')
createTrainingSet(100)

#



# file.write(",")
# for i in headers:
#     file.write(i + ",")
#
# file.write("\n")
#
# for i in DS:
#     file.write(i + ",")
#     for j in DS[i]:
#         file.write(j + ",")
#     file.write("\n")
