import pygame,time
import math
from shapes import object
from Vector2D import Vector2D
from buttons import buttons
from sticks import sticks

SCREENWIDTH = 1500
SCREENHEIGHT = 1000
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
clock = pygame.time.Clock()
bounce = 0.90
running = True
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        
class Nodes:
    def __init__(self, pos, prevPos = 0,pinned = False, acc = Vector2D(0,0), mass = 1):
        self.pos = pos
        self.prevPos = pos
        self.pinned = pinned
        self.mass = mass
        self.acc = acc
    def update(self,dt):
        #basic verlet movement
        if self.pinned == True:
            return
        tempVel = 2 * self.pos - self.prevPos
        self.prevPos = self.pos
        self.pos = tempVel + self.acc * dt**2
        self.acc = Vector2D(0,0)
        
    def accelarate(self, ROA):
       self.acc += ROA
       
    def applyForce(self,force):
        if self.pinned == True:
            return
        self.acc += force / self.mass
        
    def applyImpulse(self, impulse):
        if self.pinned == True:
            return
        self.pos+=impulse / self.mass   
        
    def resetForce(self):
        self.acc= Vector2D(0,0)
        
    def constrainPoints(self,dt):
        if self.pinned == True:
            return
        if self.pos.x > SCREENWIDTH:
            distance = self.pos - self.prevPos
            self.pos.x = 2* SCREENWIDTH - self.pos.x
            self.prevPos.x = self.pos.x + bounce * distance.x
            j = distance.y
            k = distance.x * 0.5
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.pos.y -= 2.0 * j * dt
            else:
                if k * t > 0.0:
                    self.pos.y -= k * dt
        elif self.pos.x < 0:
            distance = self.pos - self.prevPos
            self.pos.x = -self.pos.x
            self.prevPos.x = self.pos.x + bounce * distance.x
            j = distance.y
            k = distance.x * 0.5
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.pos.y -= 2.0 * j * dt
            else:
                if k * t > 0.0:
                    self.pos.y -= k * dt
        if self.pos.y > SCREENHEIGHT:
            distance = self.pos - self.prevPos
            self.pos.y = 2.0 * SCREENHEIGHT - self.pos.y 
            self.prevPos.y = self.pos.y  + bounce * distance.y 
            #
            j = distance.x
            k = distance.y * 0.5
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.pos.x -= 2.0 * j*dt 
            else:
                if k * t > 0.0:
                    self.pos.x -= k*dt
        elif self.pos.y <0 :
            distance = self.pos - self.prevPos
            self.pos.y = -self.pos.y 
            self.prevPos.y = self.pos.y  + bounce * distance.y 
            #
            j = distance.x
            k = distance.y * 0.5
            t = j
            if j != 0.0:
                t /= abs(j)
            if abs(j) <= abs(k):
                if j * t > 0.0:
                    self.pos.x -= 2.0 * j*dt 
            else:
                if k * t > 0.0:
                    self.pos.x -= k*dt    

def createCloth(listOfNodes,listOfSticks, n, m):
    # n  is aantal nodes horizontaal
    # m  is aantal nodes verticaal
    #create nodes
    for x in range(0,m):
        for y in range(0,n):
            listOfNodes.append(Nodes(pos = Vector2D(x = 300 +y*30,y =150+x*50), pinned= False))
    #create horizontal lines
    for y in range(0,m):
        for x in range(0,n-1):
            listOfSticks.append(sticks(point0= listOfNodes[x+int(y*len(listOfNodes)/m)], point1 = listOfNodes[x+int(y*len(listOfNodes)/m)+1], hidden= False)) 
    # create vertical lines
    for y in range(0,n):
        for x in range(0,m-1):
            listOfSticks.append(sticks(point0= listOfNodes[y + x * int(len(listOfNodes)/m)], point1 = listOfNodes[y + (x+1) * int(len(listOfNodes)/m)], hidden= False)) 
    for y in range(0,n):
        listOfNodes[y].pinned = True
     
def spring():
    node1 = Nodes( pos = Vector2D(10,10))
    node2 = Nodes(pos= Vector2D(200,100))
    l = []
    l.append(node1)
    l.append(node2)
    stick = []
   
    stick.append(sticks(point0 = node1, point1= node2, id = [0,1]))
    return  l,stick

def createChainBlock():
    listOfNodes = []
    listOfNodes.append(Nodes(pos = Vector2D(200,100),pinned=True))
    listOfNodes.append(Nodes(pos= Vector2D(10,120)))
    listOfNodes.append(Nodes(pos = Vector2D(120,150)))
    listOfNodes.append(Nodes(pos = Vector2D(150,120)))
    listOfNodes.append(Nodes(pos = Vector2D(100,100)))
    
    point1 = listOfNodes[0]
    point2 = listOfNodes[1]
    point3 = listOfNodes[2]
    point4 = listOfNodes[3]
    point5 = listOfNodes[4]
    
    listOfSticks = []
    listOfSticks.append(sticks(point0=point1, point1=point2,id = [0,1]))
    listOfSticks.append(sticks(point0=point3, point1=point4,id= [2,4]))
    listOfSticks.append(sticks(point0=point1, point1=point4, id = [0,3]))
    listOfSticks.append(sticks(point0=point4, point1=point2, id = [3,1]))
    listOfSticks.append(sticks(point0=point2, point1=point3,id = [1,2]))
    listOfSticks.append(sticks(point0=point3, point1=point1, id = [0,2]))
    listOfSticks.append(sticks(point0=point5, point1=point1,id = [4,0]))

    return listOfNodes, listOfSticks
def createBlock(listOfNodes, listOfSticks):
    listOfNodes.append(Nodes(pos= Vector2D(0,0), mass= 10))
    listOfNodes.append(Nodes(pos= Vector2D(0,30)))
    listOfNodes.append(Nodes(pos= Vector2D(30,30)))
    listOfNodes.append(Nodes(pos= Vector2D(30,0)))
    listOfSticks.append(sticks(point0= listOfNodes[0], point1 = listOfNodes[1],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[1], point1 = listOfNodes[2],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[2], point1 = listOfNodes[3],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[3], point1 = listOfNodes[0],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[0], point1 = listOfNodes[2],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[1], point1 = listOfNodes[3],  hidden = False))
def createBlocke(listOfNodes, listOfSticks):
    listOfNodes.append(Nodes(pos= Vector2D(0,0)))
    listOfNodes.append(Nodes(pos= Vector2D(0,300)))
    listOfNodes.append(Nodes(pos= Vector2D(300,300)))
    listOfNodes.append(Nodes(pos= Vector2D(300,0)))
    listOfSticks.append(sticks(point0= listOfNodes[0], point1 = listOfNodes[1],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[1], point1 = listOfNodes[2],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[2], point1 = listOfNodes[3],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[3], point1 = listOfNodes[0],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[0], point1 = listOfNodes[2],  hidden = False))
    listOfSticks.append(sticks(point0= listOfNodes[1], point1 = listOfNodes[3],  hidden = False))

def main():
    pygame.init()
    running = True
    listOfButtons = []
    grabbedNode = Nodes(Vector2D(0,0)) 
    
    allObjects= []
    allObjects.append(object(listOfNodes = createChainBlock()[0], listOfSticks= createChainBlock()[1]))
    #allObjects.append(object(spring()[0],spring()[1]))
    pull = False
    amountofiterations = 1
   
    button1 = buttons(x=20,y = 800,length = 200, height=25, color= WHITE, text= "increase iterations " + str(amountofiterations))
    button2 = buttons(x=20,y = 850,length = 200, height=25, color= RED, text= "decrease iterations " + str(amountofiterations))
    button3 = buttons(x=20,y = 900,length = 200, height=25, color= RED, text= "restart")
  
    listOfButtons.append(button1)
    listOfButtons.append(button2)
    listOfButtons.append(button3)
    
    timer = 0
    dt = 0
    FPS = 60
    prev_time = time.time()
    
    while running:
        clock.tick(FPS)
        now = time.time()
        dt = now- prev_time
        prev_time = now
        timer+=dt
        dt =dt*10
        mousepos= pygame.mouse.get_pos()
        mousevec = Vector2D(mousepos[0],mousepos[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pull = True
                for objects in allObjects:
                 for Node in objects.listOfNodes:
                    if Node.pos.x -10 <= mousepos[0] <= Node.pos.x+10 and Node.pos.y -10 <= mousepos[1] <= Node.pos.y+10:
                        grabbedNode = Node
                        break
                    if button1.detectClick(mousepos=mousepos) == True:
                       amountofiterations +=1
                       button1.text = "increase iterations " + str(amountofiterations)
                       button2.text = "decrease iterations " + str(amountofiterations)
                    if button2.detectClick(mousepos=mousepos) == True:
                      amountofiterations -=1
                      button1.text = "increase iterations " + str(amountofiterations)
                      button2.text = "decrease iterations " + str(amountofiterations)
                if button3.detectClick(mousepos=mousepos) == True:
                    listOfNodes = []
                    listOfSticks = []
                    createCloth(listOfSticks=listOfSticks,listOfNodes=listOfNodes,n=20,m=10)
            if event.type== pygame.MOUSEBUTTONUP:
              pull= False
              grabbedNode = Nodes(pos=Vector2D(0,0))
              
        if pull ==True:
            grabbedNode.pos = Vector2D(mousepos[0],mousepos[1])
            force = (mousevec- grabbedNode.pos)
            grabbedNode.applyImpulse(force)
          
        grabbedNode.pos = Vector2D(mousepos[0],mousepos[1])
        screen.fill((0,0,0))
       
        for x in listOfButtons:
            x.drawButton(screen)
   
        for objects in allObjects: 
         objects.applyGrav()
         objects.updateNodes(dt)
         objects.constrain(dt)
         objects.zeroAcc()
         objects.updateListOfSticks()
         
        for objects in allObjects:
         objects.updatesticks(dt)
         objects.drawSticks(screen)
         objects.drawNodes(screen)
        
    
        pygame.display.flip()
      
if __name__ == "__main__":
    main() 
