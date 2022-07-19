#Obsticle class
from VectorClass import Vector2D

class Obsticle:
    def __init__(self, positionX, positionY, size = 10):        
        self.x = positionX
        self.y = positionY
        self.position = Vector2D(self.x, self.y)
        self.size = size
        self.velocity = Vector2D()        
        self.acceleration = Vector2D()
        self.maxSpeed = 2
        self.maxForce = 0.2
    