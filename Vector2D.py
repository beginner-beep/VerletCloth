import math
class Vector2D:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x-other.x, self.y-other.y)
    
    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)
    __rmul__ = __mul__
    
    def normalize(self):
        length = self.length()
        if length !=0:
            return Vector2D(self.x/length, self.y/length)
        return Vector2D(0,0)
        
    def length(self):
        return math.sqrt(self.x **2 + self.y**2)
    
    def __truediv__(self,other):
        return Vector2D(self.x/other, self.y/other)
    
    def __neg__(self):
        return Vector2D(-self.x,-self.y)
    
    def __pos__(self):
        return Vector2D(self.x, self.y)
    
    def dotProduct(self, other):
        return self.x * other.x + self.y + other.y