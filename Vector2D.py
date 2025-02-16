import math
class Vector2D:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __add__(self, toBeAdded):
        return Vector2D(self.x + toBeAdded.x, self.y + toBeAdded.y)
    def __sub__(self, other):
        return Vector2D(self.x-other.x, self.y-other.y)
    def __mul__(self, toBeMultiplied):
        return Vector2D(self.x * toBeMultiplied, self.y * toBeMultiplied)
    __rmul__ = __mul__
    def normalize(self):
        length = self.length()
        if self.length !=0:
            return Vector2D(self.x/length, self.y/length)
        #len = math.sqrt(self.x**2 + self.y**2)
        #lpha = 1/len
        #return Vector2D(self.x * alpha, self.y * alpha)
    def length(self):
        return math.sqrt(self.x **2 + self.y**2)
    def __truediv__(self,other):
        return Vector2D(self.x/other, self.y/other)
    def __neg__(self):
        return Vector2D(-self.x,-self.y)
    def __pos__(self):
        return Vector2D(self.x, self.y)
