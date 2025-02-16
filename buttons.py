import pygame
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