import math
import numpy as np
import random

rate = .1

class Layer:
    def __init__(self, size):
        self.a = np.zeros(shape=(size,1))
        self.dotvalue = np.zeros(shape=(size,1))
        self.gradients = np.zeros(shape=(size,1))
        self.delta = np.zeros(shape=(size,1))
        self.size = size
        self.bias = np.zeros(shape=(size,1))
        for i in range(len(self.bias)):
            for j in range(len(self.bias[i])):
                num = random.uniform(-1,1)
                self.bias[i][j] = num



def acc (output,targets):
    error = 0
    for ty in range(len(targets)):
        error += (targets[ty][0]-output[ty])**2
    return error
def backprop(bist,allinputs,alltarget,sizematrix):
    weights = []
    layers = []
    error = 1000
    for i in range(len(sizematrix)-1):
        layers.append(Layer(sizematrix[i]))
        weights.append(np.zeros(shape=(sizematrix[i],sizematrix[i+1])))
    layers.append(Layer(sizematrix[i+1]))
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            for boom in range(weights[i].shape[1]):
                num = random.random() * 2 - 1
                weights[i][j,boom] = num
    # print(weights)
    # while error > 0.02:
    for i in range(len(weights)):
        print("W:", weights[i])

    for run in range(10000):
        output = []
        for ty in range(len(allinputs)):
            inputs = allinputs[ty]
            target = alltarget[ty]
            for i in range(len(layers)): # forward propagation
                if i == 0:
                    for j in range(layers[i].a.size):
                        layers[i].a[j, 0] = inputs[j]
                    continue
                cool = layers[i-1].a.transpose()
                cool2 = weights[i-1]

                matrix = np.dot(layers[i-1].a.transpose(),weights[i-1])# + layers[i].bias
                matrix = np.add(matrix.transpose(),layers[i].bias)
                # print(cool.shape,cool2.shape,matrix.shape)

                layers[i].dotvalue = matrix
                for k in range(layers[i].dotvalue.shape[0]):
                    for m in range(layers[i].dotvalue.shape[1]):
                        oops = layers[i].dotvalue[k]
                        layers[i].a[k] = A(layers[i].dotvalue[k,m])
            output.append(layers[2].a.item())

            # forward propagation done
            #Begin Backpropagation
            for i in reversed(range(1,len(layers))):
                if i == len(layers)-1:
                    for j in range(layers[i].size):
                        temp = layers[i].dotvalue.item(j)
                        temp1 = target[j]-layers[i].a.item(j)
                        layers[i].delta[j] = Aprime(temp) * temp1
                else:
                     hi = Aprime(layers[i].dotvalue.item(j))
                     hi2 = np.dot(weights[i],layers[i+1].delta)
                     hi3 = weights[i]
                     hi4 = layers[i+1].delta
                     layers[i].delta = Aprime(layers[i].dotvalue.item(j)) * np.dot(weights[i],layers[i+1].delta)
                     # print("Delta",i, ": ", layers[i].delta)
            # Backpropagation complete, time to update weights
            for layer in range(len(layers)-1):
                for i in range(weights[layer].shape[0]):
                    for j in range(weights[layer].shape[1]):
                        weights[layer][i,j] += rate*layers[layer].a[i]*layers[layer+1].delta[j]
                for j in range(sizematrix[layer+1]):
                    layers[layer+1].bias[j] += rate*layers[layer+1].delta[j]
            # print("weights: ",weights)

            # print(ty)
            # for i in range(len(layers)):
            #     print("Delta:",end=" ")
            #     for j in range(layers[i].delta.shape[0]):
            #         print(layers[i].delta[j].item(),end=" ")
            #     print()
            # for i in range(len(layers)):
            #     print("a:",end=" ")
            #     for j in range(layers[i].a.shape[0]):
            #         print(layers[i].a[j].item(),end=" ")
            #     print()
            # for i in range(len(layers)):
            #     print("dot:",end=" ")
            #     for j in range(layers[i].dotvalue.shape[0]):
            #         print(layers[i].dotvalue[j].item(),end=" ")
            #     print()
            # for i in range(len(layers)):
            #     print("bias:",end=" ")
            #     for j in range(layers[i].bias.shape[0]):
            #         print(layers[i].bias[j].item(),end=" ")
            #     print()
            # for i in range(len(weights)):
            #     print("New W:", weights[i])

            # print("*" * 60)
        # error = acc(output, alltarget)
        # print(error)
    # for i in range(len(weights)):
    #     print("W:", weights[i])


    for ty in range(len(allinputs)):
        inputs = allinputs[ty]
        for i in range(len(layers)):  # forward propagation
            if i == 0:
                for j in range(layers[i].a.size):
                    layers[i].a[j, 0] = inputs[j]
                continue
            matrix = np.dot(layers[i - 1].a.transpose(), weights[i - 1])  # + layers[i].bias
            layers[i].dotvalue = np.add(matrix.transpose(), layers[i].bias)
            for k in range(layers[i].size):
                for l in range(layers[i].a.shape[1]):
                    layers[i].a[k, l] = A(layers[i].dotvalue[k, l])
        print(layers[2].a)
    return weights

def Aprime(x):
    # res = (math.e ** (-x)) / (math.e ** x + 1)**2
    res = A(x) * (1-A(x))
    return res
def A(x):
    res = 1 / (1 + math.e ** (-x))
    return res

array = [[0,0],[0,1],[1,0],[1,1]]
target = [[0],[1],[1],[0]]
sizematrix = [2,10,1]

# weights = [np.matrix("2.0,3.0;-2.0,-4.0;1.0,-1.0"),np.matrix("1.0,2.0;-2.0,-1.0")]

# print(np.dot(np.matrix("0,0"),np.matrix("0,0;0,0")).shape)

learning = 0.1

(backprop(learning,array,target,sizematrix))
