import pickle


def process(edges):
   d = {}
   for s in edges:
      d[s] = []
   myFile = open("rrEdges.txt")
   for l in myFile:
      p = l.split()
      d[p[0]].append(p[1])
      d[p[1]].append(p[0])
   return d


def fileToArray():
   myFile = open("rrNodes.txt")
   edges, cords, cities = {}, {}, {}
   for l in myFile:
      p = l.split()
      edges[p[0]] = ""
      cords[p[0]] = [float(p[1]), float(p[2])]
   myFile = open("rrNodeCity.txt")
   for l in myFile:
      p = l.strip("/n").split()
      for n in range(0, len(p)):
         if(n>1):
            p[1] = p[1] + " " + p[n]
      cities[p[1]] = p[0]
   return edges, cords, cities


def toFile(element, fileName):
   myFile = open(fileName, "wb")
   pickle.dump(element, myFile)
   myFile.close()


      


edges, cords, cities = fileToArray()
d = process(edges)
toFile(cities, "cities.txt")
toFile(d, "edges.txt")
toFile(cords, "cords.txt")

   

