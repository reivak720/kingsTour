''''
kingsTour
author: @reivaJ
using powerful functions by Guttag,
make a king dance
'''

from collections import defaultdict
from itertools import product, combinations
import sys
import numpy as np
from random import choice
from operator import itemgetter

sys.setrecursionlimit(1500)


def merge(left, right, compare):
    '''Assumes left and right are sorted lists and
        compare defines an ordering on the elements,
    Returns a new sorted(by compare) list containing
        the same elements as (left+right) would contain'''

    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+= 1
    while (i< len(left)):
        result.append(left[i])
        i += 1
    while (j < len(right)):
        result.append(right[j])
        j += 1
    return result


def mergeSort(L, compare = lambda x, y : x< y):
    '''Assumes L a list, compare defines an ordering
            on elements of L'''

    if len(L) < 2:
        return L[:]
    else:
        middle = len(L)//2
        left = mergeSort(L[:middle], compare)
        right = mergeSort(L[middle:], compare)
        return merge(left, right, compare)


def firstWidth(arg1, arg2):
    '''Parameteres:
    arg1 & arg2: ((x, y), weight); all type: int
    compares by weight, else by y'''

    if arg1[1] != arg2[1]:
        return arg1[1] < arg2[1]
    else:
        return arg1[0][1] < arg2[0][1]



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
        for (n1, n2) in combinations(self.nodes, 2):
                if abs(n1[0] - n2[0]) <= 1 and abs(n1[1] - n2[1]) <= 1:
                    self.edges[n1][n2] = 0
                    self.edges[n2][n1] = 0


    def dist_l1_norm(self, m, n):
        '''
        Distance using norm l1: https://en.wikipedia.org/wiki/Taxicab_geometry 
        '''
        return abs(m[0] - n[0]) + abs(m[1] - n[1])
    

    def get_closest_corner(self, node):
        '''
        get the closest corner to a node
        '''
        x = 0 if node[0] < self.height/2 else self.height-1
        y = 0 if node[1] < self.width/2 else self.width-1
        return (x, y)
        

    def update_weight(self, node, path):
        '''
        update weights for children of a node based on their 
        available children and distance to corner
        '''
        corner = self.get_closest_corner(node)
        for children in self.childrenOf(node):
            available_children =sum(child not in path for child in self.childrenOf(children))
            self.edges[node][children] = \
                self.dist_l1_norm(children, corner) + \
                available_children


    def childrenOf(self, node):
       '''
       returns the children of a node
       sorts by weight of node
       if room is wider than high it will sort by y
       else by x
       '''
       if self.width/self.height > 1:
            ordered = mergeSort(list(self.edges[node].items()), firstWidth)
       else:
            ordered = sorted(self.edges[node].items(), key = itemgetter(1))
       return [child[0] for child in ordered]


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

        self.graph = BoardGraph(self.height, self.width)
        self.start = start

        if self.start not in self.graph.getNodes():
            raise ValueError ('Start possition must be within graph.')     

        self.path = self.depth_first_search(start)


    def get_start(self):
        '''returns starting point'''
        return self.start


    def get_graph(self):
        '''returns graph'''
        return self.graph


    def get_path(self):
        '''returns path'''
        return self.path


    def depth_first_search(self, start, starting_path=[]):
        '''
        recursive depth-first search
        '''
        path = starting_path + [start]
        if all(node in path for node in self.graph.getNodes()):
            return path
        self.graph.update_weight(start, path)
        for n in self.graph.childrenOf(start):
            if n not in path:
                new_path = self.depth_first_search(n, path)
                if new_path != None:
                    return new_path
 
        return None


    def represent_solution(self):
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
        print(np.flipud(model))



if __name__ == "__main__":
    height =10
    width = 10
    start = choice(list(product(range(height), range(width)))) 
    p = PathFinder(height, width, start)
    p.represent_solution()
