from heapq import heappush, heappop
from collections import deque
from string import ascii_lowercase
import time
class Node:

    def __init__(self,s,p,d,a,wset,g):
        self.state = s;
        self.parent = p;
        self.depth = d
        self.action = a
        self.wordSet = wset
        self.letters = list(ascii_lowercase)
        self.children = deque()
        self.puzzNum = len(s)
        self.goal = g
        self.goalList = self.goal.split()
        self.stateList = self.state.split()
        self.manhattan = 0

    def toString(self):
        return self.state

    def __lt__(self,value):
        return  self.manhattanDistance() < value.manhattanDistance()

    def manhattanDistance(self):
        if self.parent == None:
            total = 0
            for i in range (len(self.goalList)):
                if self.goalList[i] == self .stateList[i]:
                    total += 1
                return (self.puzzNum - total)+ self.depth
        else:
            if self.parent.state[self.action] == goal[self.action] and self.state[self.action]!= goal[self.action]:
                self.manhattan = self.parent.manhattan + 2 + self.depth
            elif self.parent.state[self.action] != goal[self.action] and self.state[self.action] != goal[self.action]:
                self.manhattan = self.parent.manhattan + 1 + self.depth
            else:
                self.manhattan = self.parent.manhattan
            return self.manhattan

    def expand(self):
        for i in range(self.puzzNum):
            for j in range(26):
                temp = self.state
                tempList = list(temp)
                tempList[i] = self.letters[j]
                temp = "".join(tempList)
                if temp in self.wordSet and temp != self.state:
                    self.children.append(Node(temp,self, self.depth +1, i, self.wordSet, self.goal))
        return self.children

    
def search(g):
    prev = set()
    while True:
        if len(fringe) == 0:
            if node.state != g:
                cool.write(g + " ")
                cool.write("- ")
            return
        node = heappop(fringe)
        if node.state == g:
            cool.write (g + " ")
            cool.write(str(node.depth) + " ")
            fringe.clear()
        else:
            children = node.expand()
            for i in range(len(children)):
                if children[i].state not in prev:
                    x = children[i].state
                    prev.add(x)
                    heappush(fringe, children[i])

start = time.time()
f = open("moreWords.txt",'r')
file = open("puxxles.txt",'r')
cool = open("solutions.txt",'w')
wordSet = set(f.read().split('\n'))
input = file.read().split('\n')

for i in input:
    start = time.time()
    x = i.split(' ')
    if len(i) == 0:
        break
    startWord = x[0]
    goal = x[1]
    fringe = []

    startState = Node(startWord, None, 0, None, wordSet, goal)
    heappush(fringe, startState)
    cool.write(startState.toString() + " ")
    search(goal)
    cool.write(str(time.time() - start) + "\n")
cool.close()