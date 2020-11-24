# author @reivaJ

from collections import defaultdict
from itertools import product
import sys
import numpy as np
from random import choice
from operator import itemgetter

sys.setrecursionlimit(1500)
class BoardGraph(object):
    '''Square room graph, connecting continous tile spaces'''

    def __init__(self, height, width): 
        '''creates a graph for a square room of dimension height x width''' 
        self.width = width
        self.height = height  
        self.nodes =  list(product(range(height), range(width)))
        self.edges = defaultdict(dict)
        self.breed()

    def breed(self):
        for node in self.nodes:
            for children in self.nodes:
                if children != node and abs(node[0] - children[0]) <=1 and abs(node[1] - children[1]) <=1:
                    self.edges[node][children] = 0


    def cornerWeight(self, child, corner):
        value = abs(child[0]-corner[0]) + abs(child[1] - corner[1])
        return value
    
    def getCorner(self, node):
        corners = [(0,0), (0, self.width - 1), (self.height-1, 0), (self.height-1, self.width-1)]
        for corner in corners:
            if abs(corner[0] - node[0]) < self.height/2 and abs(corner[1] - node[1]) < self.width/2:
                return corner 
        
    def updateWeight(self, node, path):
      
        corner = self.getCorner(node)
        for children in self.childrenOf(node):
            available_children = 0
            for child in self.childrenOf(children):                
                if child not in path:
                    available_children += 1
            available_children += self.cornerWeight(children, corner)
            self.edges[node][children] = available_children 

    def childrenOf(self, node):
       
        children = sorted(self.edges[node].items(), key = itemgetter(1))
        return[child[0] for child in children]

    def getEdges(self):
        return self.edges.keys()

    def printGraph(self):
        for node, children in self.edges.items():
            print ("Node:", node, "     Children:", children)


def loanlyCornerDepth(graph, start, path=[]): 
    node = start
    path.append(node)   
    if all(node in path for node in graph.getEdges()):
        return path    
    graph.updateWeight(node, path)
    for n in graph.childrenOf(node):
        if n not in path:
            new_path = loanlyCornerDepth(graph, n, path)
            if new_path != None:
                return path
    if len(path) != 1:
        path.remove(node)


def representSolution(solution, height, width):
    model = np.zeros((height, width), dtype = int)
    step = 1
    for coordinate in solution:
        model[coordinate] = step
        step += 1
    print(model)



if __name__ == "__main__":
    height = 10
    width = 10
    g = BoardGraph(height, width)
    start = choice(list(product(range(height), range(width))))
    print (start)
    representSolution(loanlyCornerDepth(g, start), height, width)
