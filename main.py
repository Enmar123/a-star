# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:21:24 2020

@author: js_en
"""

import numpy as np
import queue
import collections
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
        self.image = image
        self.mesh = Mesh()     # Processed nodes
        self.q = collections.deque() # Nodes to be processed
        
        self.pixel_blue = np.array([255,0,0],dtype="uint8")
        self.pixel_red = np.array([0,0,255],dtype="uint8")
        self.pixel_orange = np.array([0,165,255],dtype="uint8")
        
    def solveNextNode(self):
        current_node = self.q.popleft()
        current_position = current_node.getPosition()
        surroundings = self.getSurroundings(current_position)
        for position in surroundings:
            if self.isPositionInQueue(position):
                new_node = self.getPendingNode(position) #get node if it aready exists
            else:
                new_node = Node(position)
            new_node.addConnection(current_node)
            current_node.addConnection(new_node)
            if not self.isPositionInQueue(position) and isPixelWhite(self.image[position[0],position[1]]):
                self.addToQueue(new_node)
                self.image[position[0],position[1]] = self.pixel_orange
        self.image[current_position[0],current_position[1]] = self.pixel_blue
        self.mesh.addNode(current_node)
    
    def addToQueue(self, node):
        self.q.append(node)
        
    
    def isPositionInQueue(self, position):
        for pending_node in list(self.q):
            if pending_node.getPosition() == position:
                return True
            else:
                pass
        return False
    
    def getPendingNode(self, position):
        for pending_node in list(self.q):
            if pending_node.getPosition() == position:
                return pending_node
        
    
    def makeMesh(self, viz=False, delay=1):
        # 
        position = findStartPosition(self.image)
        first_node = Node(position)
        self.addToQueue(first_node)
        while not len(self.q) == 0:
            self.solveNextNode()
            if viz == True:
                self.showImage(delay)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
        
    def showImage(self, delay):
        image = cv.resize(self.image, (250,250),interpolation = cv.INTER_NEAREST)
        cv.imshow("Image", image)
        cv.waitKey(delay)


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
                        if ([un,vn] != [u,v]) and not isPixelBlack(self.image[un][vn]) and not isPixelBlue(self.image[un][vn]):
                            surroundings.append([un,vn])
                            #self.image[un,vn] = self.pixel_red
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

def isPixelBlue(pixel):
    blue = [255,0,0]
    mypixel = []
    for item in pixel:
        mypixel.append(item)
    if mypixel == blue:
        return True
    else:
        return False

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
    image1 = [[[255,255,255],[255,255,255],[255,255,255]],
             [[255,255,255],   [0,0,0],   [255,255,255]],
             [[255,255,255],[255,255,255],[255,255,255]]]
    image1 = np.array(image1,dtype="uint8")
    
    image2 = cv.imread("map.png")
    image2 = cv.resize(image2, (250,250),interpolation = cv.INTER_NEAREST)
    
    mm = MeshMaker(image2)
    mm.makeMesh(viz=True)
    