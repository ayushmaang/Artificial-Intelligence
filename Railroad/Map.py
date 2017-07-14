#Ayushmaan Ganotra Railroads

import pickle
import sys
import math
import time

myFile = open("edges.txt", "rb")
d = pickle.load(myFile)
myFile.close()

myFile = open("cities.txt", "rb")
cities = pickle.load(myFile)
myFile.close()

myFile = open("cords.txt", "rb")
cords = pickle.load(myFile)
myFile.close()

station1 = None
goal = None

def main():
  read()



def heuristic(y1, x1, y2, x2):
  x1 = float(x1)
  y1 = float(y1)
  x2 = float(x2)
  y2 = float(y2)
  R = 3958.76 #miles
  x1 *= (math.pi)/180.0
  y1 *= (math.pi)/180.0
  x2 *= (math.pi)/180.0
  y2 *= (math.pi)/180.0

  return math.acos(min(1,math.sin(y1)*math.sin(y2)+math.cos(y1)*math.cos(y2)*math.cos(x2-x1)))*R

cool = open("solutions.txt",'w')

def read():
  file = open("test.txt")

  s = file.read().split("\n")
  for i in s:
    i = i.split(", ")
    station1 = i[0]
    if len(i) == 1:
      break
    goal = i[1]
     # state,  depth
    cool.write (station1 + " " + goal + " ")
    station1 = cities[station1]
    goal = cities[goal]
    fringe = [(0, station1, 0)]
    closed = {}
    start = time.time()
    search(goal,fringe,closed,start)




def search(goal,fringe,closed,start):
  while(fringe): #f = f, node = state, g = ge
    element = fringe.pop(0) #pops state
    f = element[0]
    state = element[1]
    ge = element[2]

    if(state == goal):
      found = True;
      string = str(ge)

      cool.write  ("%8.3f" %(ge) + " ")
      string = str(time.time() - start)
      cool.write("%4.3f" %(time.time() - start) + "\n")
      break
    else:
      closed[state] = ge
      children = d[state]
      for c in children:
        g = heuristic(cords[state][0], cords[state][1], cords[c][0], cords[c][1])
        h = heuristic(cords[c][0], cords[c][1], cords[goal][0], cords[goal][1])
        if(c in closed):
          if(closed[c] > ge + g):
            del closed[c]
            fringe.append((ge+g+h, c, ge+g))
        else:
          b = True
          for q in fringe:
            if(c in q):
              if(q[2] > ge + g):
                fringe.remove(q)
                fringe.append((ge+g+h, c, ge+g))
              b = False
          if(b):
            temp = ge + g + h
            fringe.append((temp, c, ge+g))
    fringe.sort()


closed = {}
main()

cool.close()
