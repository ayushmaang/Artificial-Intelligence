import numpy as np
import math
import random
import time

N = 2
dims = [2,2,1]
Layer = dims
layers = range(len(Layer))
firstlayers = range(len(dims)-1)
lastlayers = range(1,len(dims))
firstlayers_rev = list(firstlayers)
lastlayers_rev = list(lastlayers)
firstlayers_rev.reverse()
rate = 0.1

def printlist(l,label):
    for j in l:
        print(label, "\n",j)
    print()

def A(x):
    return (1/(1+math.exp(-x)))
def Aprime(x):
    return A(x)*(1-A(x))
def forward_prop(x):
    global w
    global bias
    count = 0
    a = []
    dot = []
    delta = []

    for L in layers:
        a.append(np.zeros(dims[L]))
        dot.append(np.zeros(dims[L]))
        delta.append(np.zeros(dims[L]))
    for i in range(Layer[0]):
        a[0][i] = x[i]

    for L in lastlayers:
        for j in range(Layer[L]):
            dot[L][j] = sum([w[L-1][i,j] * a[L-1][i] for i in range(Layer[L-1])]) + bias[L][j]
            a[L][j] = A(dot[L][j])
        return a[N]

Av = np.vectorize(A)

def back_prop(training_set):
    global w,bias
    count = 0
    w = []
    a = []
    dot = []
    delta = []
    bias = []

    printlist(w, "W:")

    for L in firstlayers:
        w.append(np.random.normal(0,1,(dims[L],dims[L+1])))
        printlist(w,"W:")
    for L in layers:
        a.append(np.zeros(dims[L]))
        delta.append(np.zeros(dims[L]))
        bias.append([random.normalvariate[0,1] for x in range(dims[L])])

    Loss = math.inf
    start = time.time()

    while(Loss > 0.01 and count < 10000):
        Loss = 0
        for (x,y) in training_set:
            a[0] = np.array(x)

            for L in lastlayers:
                a[L] = Av(np.matmul(a[L-1],w[L-1] + bias[L]))
            delta[N] = a[N] * (1-a[N]) * (y-a[N])

            for L in firstlayers_rev:
                delta[L] = a[L]*(1-a[L]) * \
                        np.matmul(delta[L+1],w[L].transponse())
                w[L] += rate * np.outer(a[L],delta[L+1])
                bias[L+1] += rate * delta[L+1]

            Loss += 0.5 * np.matmul((a[N]-y),(a[N]-y))
            
            #printlist(a,"a: ")
            #printlist(dot,"dot: ")
            # printlist(delta,"delta: ")
            # printlist(w,"new W:")
            # printlist(bias, "bias: ")
            # print("*"*50)
        count+=1
        if(count%1000 == 0):
            print ("Loss = ", Loss)
            print("Time = ",time.time()-start)
            start = time.time()

    for(x,y) in ts:
        print(x,y,forward_prop(x))
    ts =
