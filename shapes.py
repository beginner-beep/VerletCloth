import pygame
from Vector2D import Vector2D

class object():
    def __init__(self,listOfNodes = [], listOfSticks = []):
        self.listOfNodes = listOfNodes
        self.listOfSticks = listOfSticks
   
    def updateListOfSticks(self):
        for stick in self.listOfSticks:
            stick.point0 = self.listOfNodes[stick.id[0]]
            stick.point1 = self.listOfNodes[stick.id[1]]
            
    def drawSticks(self,screen):
        for stick in self.listOfSticks:
           stick.drawStick(screen)    
            
    def drawNodes(self,screen):
        for node in self.listOfNodes:
            pygame.draw.circle(screen, [255,255,0], [node.pos.x,node.pos.y], 3)
            
    def updatesticks(self,dt):
     for stick in self.listOfSticks:
         stick.updatestick(dt)
         
    def updateNodes(self,dt):
        for node in self.listOfNodes:
            node.update(dt)
            
    def applyGrav(self):
        for node in self.listOfNodes:
            node.acc += Vector2D(0,9.81)
            
    def constrain(self,dt):
        for node in self.listOfNodes:
            node.constrainPoints(dt)
            
    def zeroAcc(self):
        for node in self.listOfNodes:
            node.acc = Vector2D(0,0)