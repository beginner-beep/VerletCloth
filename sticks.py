import math
import pygame
class  sticks:
    def __init__(self,point0,point1,id, hidden = False, stickType = 0, distance =0):
        self.point0 = point0
        self.point1 = point1
        self.id = id
        if distance == 0:
         self.distance = self.distanceF()
        else:
          self.distance = distance
        self.hidden = hidden
        self.stickType = stickType
    def updatestick(self, dt):
     damping = 0.9

     difference = self.point1.pos - self.point0.pos
     force = 0.5 * (difference.length() - self.distance) * difference.normalize() * damping

     if self.point0.pinned != True and self.point1.pinned == True:
        self.point0.applyImpulse(2 * +force * dt)
     elif self.point0.pinned != False and self.point1.pinned != True:
        self.point1.applyImpulse(2 * -force * dt)
     else:
        self.point0.applyImpulse(+force * dt)
        self.point1.applyImpulse(-force * dt)

  
    def drawStick(self, screen):
      if self.hidden == True:
        return
      pygame.draw.line(screen, (150, 150, 150), 
                     (self.point0.pos.x, self.point0.pos.y), 
                     (self.point1.pos.x, self.point1.pos.y), 
                     width=3)
    
    def distanceF(self):
     dx = self.point0.pos.x - self.point1.pos.x
     dy = self.point0.pos.y - self.point1.pos.y
     distance = math.sqrt(dx * dx + dy * dy)
     return distance
