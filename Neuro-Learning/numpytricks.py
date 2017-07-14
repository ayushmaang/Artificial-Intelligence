import numpy as np

class NN:
    def __init__(self,m):
        self.matrix = m
    def A(self,x):
        return x



def boi(array):
    t2 = np.c_[array,1]

    print(t2)

array = np.array([4,3,4,2,6])

boi(array)
