# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:21:24 2020

@author: js_en
"""

import numpy

class Node:
    def __init__(self, position):
        self.name = None # Specify unique name
        self.position = position
        self.connections = []
    
    def get_coords(self):
        return self.xyz
        
        
class Mesh:
    def __init__(self):
        self._nodes = []
        
    def __getitem__(self, item):
        return self._nodes[item]
        
    def add_node(self, node):
        self.nodes.append(node)
        

def matrix_to_mesh(image):
    # Transforms an image into an 8-mesh representation
    mesh = Mesh()
    image = [[[255,255,255],[255,255,255],[255,255,255]],
             [[255,255,255],   [0,0,0],   [255,255,255]],
             [[255,255,255],[255,255,255],[255,255,255]]]
    
    u,v = findStartPosition(image)
    node = Node([u,v])
    node_queue = []
    node_queue.append(node)
    
    getSurroundings([u,v], image)
    
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
            pixel = image[un][vn]
            if (0 <= un <= height) and (0 <= vn <= width) and ([un,vn] != [u,v]) and isPixelWhite(pixel):
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
    