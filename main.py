# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:21:24 2020

@author: js_en
"""

import numpy as np
import queue
import cv2 as cv

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
        self.image = cv.resize(np.array(image,dtype="uint8"), (250,250),interpolation = cv.INTER_NEAREST)
        self.mesh = Mesh()
        self.q = queue.Queue()
        
        self.pixel_blue = np.array([255,0,0],dtype="uint8")
        self.pixel_red = np.array([0,0,255],dtype="uint8")
        
    def solveNextNode(self):
        current_node = self.q.get()
        current_position = current_node.getPosition()
        self.image[current_position[0],current_position[1]] = self.pixel_blue #set node to "blue" color to know it is complete
        surroundings = self.getSurroundings(current_position)
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
            self.showImage()
            #print("solving node")
        #print("finished mesh")
        cv.destroyAllWindows()
        
    def showImage(self):
        cv.imshow("Image", self.image)
        cv.waitKey(1)


    def getSurroundings(self, uv):
        # Retuns a list of viable surrounding locations
        surroundings = []
        u,v = uv
        height = len(self.image)
        width = len(self.image[0])
        for i in range(3):
            un = (u - 1) + i
            if (0 <= un < height):
                for j in range(3):
                    vn = (v - 1) + j    
                    if (0 <= vn < width):
                        if ([un,vn] != [u,v]) and isPixelWhite(self.image[un][vn]):
                            surroundings.append([un,vn])
                            self.image[un,vn] = self.pixel_red
                    else:
                        pass
            else:
                pass
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

if __name__=="__main__":
    image = [[[255,255,255],[255,255,255],[255,255,255]],
             [[255,255,255],   [0,0,0],   [255,255,255]],
             [[255,255,255],[255,255,255],[255,255,255]]]
    image = cv.imread("map2.png")
    mm = MeshMaker(image)
    mm.makeMesh()
    