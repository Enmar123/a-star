# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:21:24 2020

@author: js_en
"""

import numpy as np
import queue 

class Node:
    def __init__(self, position):
        self.name = None # Specify unique name
        self.position = position
        self.connections = []
    
    def getPosition(self):
        return self.position
    
    def addConnection(self, node):
        self.connections.append(node)
        
        
class Mesh:
    def __init__(self):
        self.nodes = []
        
    def __getitem__(self, item):
        return self.nodes[item]
        
    def addNode(self, node):
        self.nodes.append(node)
        
class MeshMaker:
    def __init__(self, image):
        self.image = image
        self.mesh = Mesh()
        self.q = queue.Queue()
        
    def solveNextNode(self):
        if not self.q.empty():
            current_node = self.q.get()
            u,v = current_node.getPosition()
            self.image[u][v] = [255,0,0] #set node to "red" color to know it is complete
            surroundings = getSurroundings(current_node.getPosition(), self.image)
            for position in surroundings:
                new_node = Node(position)
                new_node.addConnection(current_node)
                current_node.addConnection(new_node)
                self.q.put(new_node)
            self.mesh.addNode(current_node)
            
        
    def makeMesh(self):
        position = findStartPosition(self.image)
        first_node = Node(position)
        self.q.put(first_node)
        while not self.q.empty():
            self.solveNextNode()
            print("solving node")
        print("finished mesh")

def matrix_to_mesh():
    # Transforms an image into an 8-mesh representation
    mesh = Mesh()
    image = [[[255,255,255],[255,255,255],[255,255,255]],
             [[255,255,255],   [0,0,0],   [255,255,255]],
             [[255,255,255],[255,255,255],[255,255,255]]]
    
    position = findStartPosition(image)
    first_node = Node(position)
    q = queue.Queue(first_node)
    if not q.empty():
        current_node = q.get()
        surroundings = getSurroundings(current_node.getPosition(), image)
        for position in surroundings:
            new_node = Node(position)
            new_node.addConnection(current_node)
            current_node.addConnection(new_node)
            q.put(new_node)
        mesh.addNode(current_node)
        u,v = current_node.getPosition()
        image[u][v] = [255,0,0] #set node to "red" color to know it is complete
        
    
    
    
    mesh.append(Node([u,v]))


def getSurroundings(uv, image):
    # Retuns a list of viable surrounding locations
    surroundings = []
    u,v = uv
    height = len(image)
    width = len(image[0])
    for i in range(3):
        un = (u - 1) + i
        for j in range(3):
            vn = (v - 1) + j
            if (0 <= un < height) and (0 <= vn < width) and ([un,vn] != [u,v]) and isPixelWhite(image[un][vn]):
                surroundings.append([un,vn])
    return surroundings 
    
def findStartPosition(image):
    # Returns the first position in an image that can be used
    u,v = 0,0
    for row in image:
        for pixel in row:
            if isPixelWhite(pixel):
                return [u,v]
            else:
                pass
            v+=1
        u+=1
    return None 

def isPixelWhite(pixel):
    for item in pixel:
        if item != 255:
            return False
    return True
        
def isPixelBlack(pixel):
    for item in pixel:
        if item != 0:
            return False
    return True
    