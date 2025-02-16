import pygame
from Vector2D import Vector2D
pygame.font.init()
import math
SCREENWIDTH = 1500
SCREENHEIGHT = 1000
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
clock = pygame.time.Clock()
bounce = 0.95
gravity = 0.5
running = True
font = pygame.font.SysFont("comic sans ms", 15 )
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
dt = 1

class buttons:
    def __init__(self,x,y,length,height,color,text):
      self.x = x
      self.y = y
      self.length = length
      self.height = height
      self.color = color
      self.text = text
    def detectClick(self,mousepos):
        if self.x <= mousepos[0] <= self.x + self.length and self.y <= mousepos[1] <= self.y + self.height:
            return True
    def drawButton(self):
        button = pygame.Rect(self.x, self.y, self.length , self.height)
        label = font.render(self.text,1, BLACK)
        
        pygame.draw.rect(screen, self.color, button)
        dis = pygame.Surface.subsurface(screen,button)
        dis.blit(label, (0, 0))
        
class Nodes:
    def __init__(self, pos, prevPos = 0,pinned = False,vel = Vector2D(0,0), acc = Vector2D(0,0), mass = 1):
        self.pos = pos
        self.prevPos = pos
        self.vel = vel
        self.pinned = pinned
        self.mass = mass
        self.acc = acc
    def update(self):
        #basic verlet movement
        if self.pinned == True:
            return
        self.vel = 2 * self.pos - self.prevPos
        self.prevPos = self.pos
        self.pos = self.vel + self.acc * dt**2
        self.vel = self.pos - self.prevPos
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
        self.pos+=impulse/self.mass   
        
    def resetForce(self):
        self.acc= Vector2D(0,0)
        
    def constrainPoints(self):
        if self.pinned == True:
            return
        
        velx = self.pos.x - self.prevPos.x
        vely = self.pos.y - self.prevPos.y
       
        if self.pos.x > SCREENWIDTH:
            self.pos.x = SCREENWIDTH
            self.prevPos.x = self.pos.x + velx * bounce
        elif self.pos.x < 0:
            self.pos.x = 0
            self.prevPos.x = self.pos.x + velx * bounce
        if self.pos.y > SCREENHEIGHT:
            self.pos.y = SCREENHEIGHT
            self.prevPos.y = self.pos.y + vely * bounce
        elif self.pos.y <0 :
            self.pos.y = 0
            self.prevPos.y = self.pos.y + vely * bounce           
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
            listOfSticks.append(sticks(point0= listOfNodes[x+int(y*len(listOfNodes)/m)], point1 = listOfNodes[x+int(y*len(listOfNodes)/m)+1], distance= distance(p0= listOfNodes[x+int(y*len(listOfNodes)/m)], p1= listOfNodes[x+int(y*len(listOfNodes)/m)+1]), hidden= False)) 
    # create vertical lines
    for y in range(0,n):
        for x in range(0,m-1):
            listOfSticks.append(sticks(point0= listOfNodes[y + x * int(len(listOfNodes)/m)], point1 = listOfNodes[y + (x+1) * int(len(listOfNodes)/m)], distance= distance(p0= listOfNodes[y + x * int(len(listOfNodes)/m)], p1= listOfNodes[y + (x+1) * int(len(listOfNodes)/m)]), hidden= False)) 
    for y in range(0,n):
        listOfNodes[y].pinned = True
    
class  sticks:
    def __init__(self,point0,point1,distance, hidden):
        self.point0 = point0
        self.point1 = point1
        self.distance = distance
        self.hidden = hidden
        
def distance(p0,p1):
    dx = p0.pos.x - p1.pos.x
    dy = p0.pos.y- p1.pos.y
    distance = math.sqrt(dx* dx + dy* dy)
    return distance
def fillShape(listOfNodes):
    pol = listOfNodes[0:10]
    pol.append(listOfNodes[11:20])
    pygame.draw.polygon(screen,[255,255,255], pol)
def drawSticks(listofsticks):
    for stick in listofsticks:
        if stick.hidden == True :
            continue
        pygame.draw.line(screen, (150,150,150), (stick.point0.pos.x,stick.point0.pos.y), (stick.point1.pos.x , stick.point1.pos.y), width = 3)      
      
def drawNodes(listOfNodes):
  for Node in listOfNodes:
     pygame.draw.circle(screen,[255,255,0], (Node.pos.x,Node.pos.y), 5)
     
def updatesticks(listofsticks):
    for index, stick in enumerate(listofsticks):
        difference = stick.point1.pos - stick.point0.pos
        force = 0.5 *(difference.length() - stick.distance) * difference.normalize()
        
        if stick.point0.pinned != True and  stick.point1.pinned == True:
            stick.point0.applyImpulse(2.0 * +force)
        elif  stick.point0.pinned != False and stick.point1.pinned != True:
            stick.point1.applyImpulse(2.0 * -force)
        else:
         stick.point0.applyImpulse(+force)
         stick.point1.applyImpulse(-force)
      
def createChainBlock(listOfNodes,listOfSticks):
    listOfNodes.append(Nodes(pos = Vector2D(200,100),pinned=True))
    listOfNodes.append(Nodes(pos= Vector2D(10,120),pinned=True))
    listOfNodes.append(Nodes(pos = Vector2D(120,150),pinned=True))
    listOfNodes.append(Nodes(pos = Vector2D(150,120),pinned=True))
    listOfNodes.append(Nodes(pos = Vector2D(100,100), pinned = True))
    point1 = listOfNodes[0]
    point2 = listOfNodes[1]
    point3 = listOfNodes[2]
    point4 = listOfNodes[3]
    point5 = listOfNodes[4]
    
    listOfSticks.append(sticks(point0= point1, point1 = point2, distance= distance(p0= point1, p1= point2), hidden= False))
    listOfSticks.append(sticks(point0= point3, point1 = point4, distance= distance(p0= point3, p1= point4), hidden= False))
    listOfSticks.append(sticks(point0= point1, point1 = point4, distance= distance(p0= point1, p1= point4), hidden = False))
    listOfSticks.append(sticks(point0= point4, point1 = point2, distance= distance(p0= point4, p1= point2), hidden = False))
    listOfSticks.append(sticks(point0= point2, point1 = point3, distance= distance(p0= point3, p1= point2) , hidden = False))
    listOfSticks.append(sticks(point0= point3, point1 = point1, distance= distance(p0= point1, p1= point3), hidden = False))
    listOfSticks.append(sticks(point0= point5, point1 = point1, distance= distance(p0= point1, p1= point4), hidden = False))  
def calc(listOfNodes, listOfSticks):
    for Node in listOfNodes:
       Node.update()   
    updatesticks(listOfSticks)
def main():
    pygame.init()
    running = True
    listOfNodes = []
    listOfSticks =[]  
    listOfButtons = []
    grabbedNode = Nodes(Vector2D(0,0))
    createChainBlock(listOfNodes,listOfSticks)
    pull = False
    amountofiterations = 5
   # createCloth(listOfNodes,listOfSticks, n = 20, m = 10)
   
    button1 = buttons(x=20,y = 800,length = 200, height=25, color= WHITE, text= "increase iterations " + str(amountofiterations))
    button2 = buttons(x=20,y = 850,length = 200, height=25, color= RED, text= "decrease iterations " + str(amountofiterations))
    button3 = buttons(x=20,y = 900,length = 200, height=25, color= RED, text= "restart")
  
    listOfButtons.append(button1)
    listOfButtons.append(button2)
    listOfButtons.append(button3)
    while running:
        dt = clock.tick(30) /1000
        mousepos= pygame.mouse.get_pos()
        mousevec = Vector2D(mousepos[0],mousepos[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pull = True
                for Node in listOfNodes:
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
            
        for Node in listOfNodes:
            Node.accelarate(ROA = Vector2D(0,9.81))
            Node.update()
            
        for x in range(amountofiterations):    
          for Node in listOfNodes:
            Node.constrainPoints()
          updatesticks(listOfSticks)
        grabbedNode.pos = Vector2D(mousepos[0],mousepos[1])
        screen.fill((0,0,0))
       # fillShape(listOfNodes)
        for x in listOfButtons:
            x.drawButton()
        drawNodes(listOfNodes)
        drawSticks(listOfSticks)
        pygame.display.flip()
      
if __name__ == "__main__":
    main() 
