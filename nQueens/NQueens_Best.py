# Ayushmaan Ganotra
# Block: 4
# Email: ayushmaang@gmail.com


import time
import math
import heapq
import random
from collections import deque
import random
from copy import deepcopy
class nQueens:
    def __init__(self, state=None, choices=None, n=8):
        """Creates nQueens"""
        self.n=n
        if(state is not None):
            self.state=state
        else:
            self.state=n*[n]
        if choices == None:
            self.choices = list()
            for i in range(self.n):
                s = set()
                for j in range(self.n):
                    s.add(j)
                self.choices.append(s)
        else:
            self.choices = choices

    def assign(self, var, value):
        """ updates the state by setting state[var] to value
            also propgates constraints and updates choices
        """
        self.state[var] = value
        self.choices[var]=set()
        for i in self.choices:
            """Updates Choices by removing the same row"""
            i.difference_update({value})
        num=0
        for i in self.choices:
            """Updates Chocies by removing diagonals"""
            i.difference_update({(value+(var-num))})
            i.difference_update({(value-(var-num))})
            num = num+1

    def goal_test(self):
        if self.n not in self.state:
            return True
        return False

    def get_next_unassigned_var(self):
        """ returns the index of a column that is unassigned and
            has valid choices available, checks which column has
            the least nubmer of choices and selects that one,
            ties are solved by whichever index was picked first"""

        index = self.n
        minChoices = self.n +1
        for i in range(len(self.choices)):
            if len(self.choices[i]) < minChoices and self.state[i] == self.n:
                index = i
                minChoices = len(self.choices[index])
                if len(self.choices[index]) == 0 and self.state[index] is self.n:
                    return self.n
        return index

    def get_choices_for_var(self, var):
        """ returns choices[var], the list of available values
                 for variable var, uses random method to sort random choices"""
        ch = list(self.choices[var])
        ch = self.h1(ch)
        return ch

    def h1(self,ch):
        """Creates random sorted choices"""
        return sorted(ch,key=lambda i : random.random())

    def h2(self,a):
        """Creates choices sorted from right, did not use"""
        return sorted(a,key = lambda i: abs(i-self.n))


    def __str__(self):
        """ returns a string representation of the object """
        s = ""
        for i in range(self.n):
            for j in range(self.n):
                if self.state[j] == i:
                    s+= "|Q|"
                else:
                    s+="|_|"
            s+= "\n"

        return s

def dfs_search(board):
    """ sets board as the initial state and returns a
        board containing an nQueens solution
        or None if none exists
    """
    fringe = []
    fringe.append(board)
    count = 0
    goal = 0
    while True:
        goal+=1
        if (len(fringe)==0):
            return None
        current=fringe.pop()
        if(current.goal_test()):
            cool.write(str(goal) + ",")
            cool.write(str(count) + ",")
            return current
        if count >= 1000000:
            return cool.write("Too Slow!,")
        if count == 0:
            var = 1
        else:
            var=current.get_next_unassigned_var()

        if var == current.n:
            continue

        for value in current.get_choices_for_var(var):
            newchoices = [set(x) for x in current.choices]
            child = nQueens(current.state[:],newchoices,current.n)
            child.assign(var, value)
            fringe.append(child)
            count+=1
        current = None

N=150
cool = open("solutions_150.csv",'w')
total = time.time()
node = nQueens(None, None, N)
start=time.time()
cool.write(str(N) + ",")
dfs_search(node)
end=time.time()
cool.write(str(end-start) + ",\n")
print(str(end-start))

cool.close()
