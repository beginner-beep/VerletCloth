import pygame
import math
SCREENWIDTH = 1000
SCREENHEIGHT = 1000

clock = pygame.time.Clock()
bounce = 0.95
gravity = 0.5
running = True
class Nodes:
    def __init__(self, x, y, prevx, prevy, pinned):
        self.x = x
        self.y = y 
        self.prevx = prevx
        self.prevy = prevy
        self.pinned = pinned
        
    def update(self):
        #basic verlet movement
        if self.pinned == True:
            return
        
        velx = self.x - self.prevx
        vely = self.y - self.prevy
        self.prevx = self.x
        self.prevy = self.y
        self.x += velx 
        self.y += vely
        self.y += gravity
     
    def constrainPoints(self):
        if self.pinned == True:
            return
        
        velx = self.x - self.prevx
        vely = self.y - self.prevy
       
        if self.x > SCREENHEIGHT:
            self.x = SCREENHEIGHT
            self.prevx = self.x + velx * bounce
        elif self.x < 0:
            self.x = 0
            self.prevx = self.x + velx * bounce
        if self.y > SCREENWIDTH:
            self.y = SCREENWIDTH
            self.prevy = self.y + vely * bounce
        elif self.y <0 :
            self.y = 0
            self.prevy = self.y + vely * bounce
def createCloth(listOfNodes,listOfSticks):
   
    for x in range(10,20):
        for y in range(0,10):
            listOfNodes.append(Nodes(x = x*30,y =150+y*50, prevx= 150, prevy = 150, pinned= False))
    for x in range(0,10):
        listOfNodes[x*10].pinned = True
    for N in range(0,10):
        for x in range(N*10,N*10+9):
            listOfSticks.append(sticks(point0= listOfNodes[x], point1 = listOfNodes[x+1], distance= distance(p0= listOfNodes[x], p1= listOfNodes[x+1]), hidden= False)) 
            try:
                listOfSticks.append(sticks(point0= listOfNodes[x], point1 = listOfNodes[x+10], distance= distance(p0= listOfNodes[x], p1= listOfNodes[x+10]), hidden= False)) 
            except:
                continue
    for x in range(0,90, 10):
        listOfSticks.append(sticks(point0= listOfNodes[x+9], point1 = listOfNodes[x+19], distance= distance(p0= listOfNodes[x+9], p1= listOfNodes[x+19]), hidden= False)) 
    
class  sticks:
    def __init__(self,point0,point1,distance, hidden):
        self.point0 = point0
        self.point1 = point1
        self.distance = distance
        self.hidden = hidden
def distance(p0,p1):
    dx = p0.x - p1.x
    dy = p1.y - p0.y
    distance = math.sqrt(dx* dx + dy* dy)
    return distance

def drawSticks(listofsticks,screen):
    for stick in listofsticks:
        if stick.hidden == True :
            continue
        pygame.draw.line(screen, (150,150,150), (stick.point0.x,stick.point0.y), (stick.point1.x , stick.point1.y), width = 3)      
      
def drawNodes(listOfNodes, screen):
  for Node in listOfNodes:
     pygame.draw.circle(screen,[255,255,0], (Node.x,Node.y), 5)
     
def updatesticks(listofsticks):
    for index, stick in enumerate(listofsticks):
        if stick.point0.pinned == True:
            dx = stick.point1.x - stick.point0.x
            dy = stick.point1.y - stick.point0.y
            distance = math.sqrt(dx*dx + dy*dy)
            difference = stick.distance - distance
            percent = difference/distance/2
            offsetx = dx* percent
            offsety = dy * percent
            stick.point1.x += offsetx
            stick.point1.y += offsety
        else:
            dx = stick.point1.x - stick.point0.x
            dy = stick.point1.y - stick.point0.y
            distance = math.sqrt(dx*dx + dy*dy)
            difference = stick.distance - distance
            percent = difference/distance/2
            offsetx = dx* percent
            offsety = dy * percent
            stick.point0.x -= offsetx
            stick.point0.y -= offsety
            stick.point1.x += offsetx
            stick.point1.y += offsety
def createChainBlock(listOfNodes,listOfSticks):
    listOfNodes.append(Nodes(x = 150,y =150, prevx= 145, prevy = 145, pinned= False))
    listOfNodes.append(Nodes(x = 120,y =120, prevx= 120, prevy = 120, pinned = False))
    listOfNodes.append(Nodes(x = 120,y =150, prevx= 120, prevy = 150, pinned=False))
    listOfNodes.append(Nodes(x = 150,y =120, prevx= 150, prevy = 120, pinned= False))
    listOfNodes.append(Nodes(x = 100, y = 100, prevx = 0, prevy = 0, pinned = True))
    point1 = listOfNodes[0]
    point2 = listOfNodes[1]
    point3 = listOfNodes[2]
    point4 = listOfNodes[3]
    point5 = listOfNodes[4]
    
    listOfSticks.append(sticks(point0= point1, point1 = point2, distance= distance(p0= point1, p1= point2), hidden= True))
    listOfSticks.append(sticks(point0= point3, point1 = point4, distance= distance(p0= point3, p1= point4), hidden= True))
    listOfSticks.append(sticks(point0= point1, point1 = point4, distance= distance(p0= point1, p1= point4), hidden = False))
    listOfSticks.append(sticks(point0= point4, point1 = point2, distance= distance(p0= point4, p1= point2), hidden = False))
    listOfSticks.append(sticks(point0= point2, point1 = point3, distance= distance(p0= point3, p1= point2) , hidden = False))
    listOfSticks.append(sticks(point0= point3, point1 = point1, distance= distance(p0= point1, p1= point3), hidden = False))
    listOfSticks.append(sticks(point0= point5, point1 = point1, distance= distance(p0= point1, p1= point4), hidden = False))  

def main():
    pygame.init()
    running = True
    listOfNodes = []
    listOfSticks =[]
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    
    createCloth(listOfNodes,listOfSticks)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        screen.fill((0,0,0))
        clock.tick(30)
        
        for Node in listOfNodes:
            Node.update()
            
        updatesticks(listOfSticks)
       
        for Node in listOfNodes:
            Node.constrainPoints()
            
        updatesticks(listOfSticks)
       
        for Node in listOfNodes:
            Node.constrainPoints()
        updatesticks(listOfSticks)

        drawNodes(listOfNodes, screen)
        drawSticks(listOfSticks,screen)
        pygame.display.flip()
      
if __name__ == "__main__":
    main() 


