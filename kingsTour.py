# author @reivaJ

from collections import defaultdict
from itertools import product
import sys
import numpy as np
from random import choice
from operator import itemgetter

sys.setrecursionlimit(1500)
class BoardGraph(object):
    '''
    Square room graph, connecting continous tile spaces
    '''
    def __init__(self, height, width): 
        '''
        Parameters:
        height: type int
        width: type int
        creates a graph for a square room of dimension height x width
        ''' 
        self.width = width
        self.height = height  
        self.nodes =  list(product(range(height), range(width)))
        self.edges = defaultdict(dict)
        self.breed()

    def breed(self):
        '''
        Connects nodes and children
        '''
        for node in self.nodes:
            for children in self.nodes:
                if children != node and abs(node[0] - children[0]) <=1 and abs(node[1] - children[1]) <=1:
                    self.edges[node][children] = 0


    def cornerWeight(self, child, corner):
        '''
        the closer the coordinate is to the corner, lower value
        '''
        value = abs(child[0]-corner[0]) + abs(child[1] - corner[1])
        return value
    
    def getCorner(self, node):
        '''
        get the closest corner to a node
        '''
        corners = [(0,0), (0, self.width - 1), (self.height-1, 0), (self.height-1, self.width-1)]
        for corner in corners:
            if abs(corner[0] - node[0]) < self.height/2 and abs(corner[1] - node[1]) < self.width/2:
                return corner 
        
    def updateWeight(self, node, path):
        '''
        update weights for children of a node based on their 
        available children and distance to corner
        '''
        corner = self.getCorner(node)
        for children in self.childrenOf(node):
            available_children = 0
            for child in self.childrenOf(children):                
                if child not in path:
                    available_children += 1
            available_children += self.cornerWeight(children, corner)
            self.edges[node][children] = available_children 

    def childrenOf(self, node):
       '''
       returns the children of a node
       '''
       children = sorted(self.edges[node].items(), key = itemgetter(1))
       return[child[0] for child in children]

    def getNodes(self):
        '''
        returns nodes in graph
        '''
        return self.nodes
    
    def getEdges(self):
        '''
        returns self.edges
        '''
        return self.edges

    def printGraph(self):
        '''
        prints nodes and children
        '''
        for node, children in self.edges.items():
            print ("Node:", node, "     Children:", children)


class PathFinder(object):

    def __init__(self, height, width, start):
        '''
        Parameters:
        height = type int
        width = type int
        start = type tuple (y<height, x<width)
        gets path between a starting point within a graph
        passing by all nodes
        '''
        self.height = height
        self.width = width
        self.graph = BoardGraph(height, width)
        if start not in self.graph.getNodes():
            raise ValueError ('Start possition must be within graph.')
        self.start = start
        self.path = self.goDeep(start)

    def get_start(self):
        '''
        returns starting point
        '''
        return self.start
    
    def get_graph(self):
        '''
        returns graph
        '''
        return self.graph
    
    def get_path(self):
        '''
        returns path
        '''
        return self.path

    def goDeep(self, start, path=[]): 
        '''
        recursive deapht-first search
        '''
        node = start
        path.append(node)   
        if all(node in path for node in self.graph.getNodes()):
            return path    
        self.graph.updateWeight(node, path)
        for n in self.graph.childrenOf(node):
            if n not in path:
                new_path = self.goDeep(n, path)
                if new_path != None:
                    return path
        if len(path) != 1:
            path.remove(node)


    def representSolution(self):
        '''
        represents path as an array
        1 is starting point and largest number
        is end point
        '''
        model = np.zeros((self.height, self.width), dtype = int)
        step = 1
        for coordinate in self.path:
            model[coordinate] = step
            step += 1
        print(model)



if __name__ == "__main__":
    height = 10
    width = 10
    start = choice(list(product(range(height), range(width)))) 
    p = PathFinder(height, width, start)
    p.representSolution()
