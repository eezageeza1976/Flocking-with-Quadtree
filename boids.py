import VectorClass
from VectorClass import Vector2D
import random
import pygame as pg
import consts
import math
from quadtree import Quadtree, Rectangle, Point



class Boid:
    def __init__(self):
        self.position = Vector2D()
        self.x = random.randrange(0, consts.WIN_WIDTH)
        self.y = random.randrange(0, consts.WIN_HEIGHT)
        self.position = Vector2D(self.x, self.y)
        self.velocity = VectorClass.random_vector()        
        self.acceleration = Vector2D()
        self.maxSpeed = 3.0
        self.maxForce = 0.1
        
    def distanceToCentre(self, centre):
        return math.sqrt((centre.x - self.x)**2 + (centre.y - self.y)**2)
  
        
def alignment(boid, flock, obsticle_list):
    align_perception_radius = 30.0           #Field of view for boid
    cohes_perception_radius = 5.0
    sep_perception_radius = 20.0
    align_steering = Vector2D()       #Steering vector to return
    cohes_steering = Vector2D()
    sep_steering = Vector2D()
    align_totalInView = 0                   #Amount of 'other' boids in view
    cohes_totalInView = 0
    sep_totalInView = 0
    total_steering = Vector2D()
    
    for others in flock:
        d = VectorClass.dist(boid.position, others.position)   #Checking position to nearest boid    
        if others != boid and d < align_perception_radius:      #If not itself and within FoV
            align_steering = align_steering + others.velocity        #Add my vector with the 'other' boid
            align_totalInView += 1                             #Inc amount of others in FoV 
        if others != boid and d < cohes_perception_radius:
            cohes_steering = cohes_steering + others.position  #to calculate cohesion
            cohes_totalInView += 1
        if others != boid and d < sep_perception_radius:      #If not itself and within FoV  
            diff = boid.position - others.position
            if d != 0:
                diff = diff / (d * d)
            sep_steering = sep_steering + diff        
            sep_totalInView += 1                             #Incr amount of others in FoV 

              
    if align_totalInView > 0:                                  #If there is at least one in FoV
        align_steering = align_steering / align_totalInView                #Divide by total in view    
        align_steering = VectorClass.set_mag(align_steering, boid.maxSpeed)
        align_steering = align_steering - boid.velocity
        align_steering = VectorClass.limit(align_steering, boid.maxForce)
        
    if cohes_totalInView > 0:                                  #If there is at least one in FoV
        cohes_steering = cohes_steering / cohes_totalInView                #Divide by total in view
        cohes_steering = cohes_steering - boid.position
        if VectorClass.length(cohes_steering) != 0:            #Check if magnitude is not 0     
            cohes_steering = VectorClass.set_mag(cohes_steering, boid.maxSpeed)    #Set all magnitudes to the same length
        cohes_steering = cohes_steering - boid.velocity
        if VectorClass.length(cohes_steering) > boid.maxForce:
            cohes_steering = VectorClass.set_mag(cohes_steering, boid.maxForce)

    if sep_totalInView > 0:                                  #If there is at least one in FoV
        sep_steering = sep_steering / sep_totalInView                #Divide by total in view
        sep_steering = VectorClass.set_mag(sep_steering, boid.maxSpeed)
        sep_steering = sep_steering - boid.velocity
        sep_steering = VectorClass.limit(sep_steering, boid.maxForce)

    avoid_steering = avoidance(boid, obsticle_list)
    total_steering = align_steering + cohes_steering + sep_steering + avoid_steering
    
    return total_steering     

def avoidance(boid, obsticle_list):
    avoid_range = 60
    avoid_steering = Vector2D()
    obs_in_range = 0
    
    for obs in obsticle_list:
        d = VectorClass.dist(boid.position, obs.position) #check if boid is close to an obsticle
        if d < avoid_range:
            diff = boid.position - obs.position
            if d != 0:
                diff = diff / (d * d)
            avoid_steering = avoid_steering + diff        
            obs_in_range += 1
        
    if obs_in_range > 0:                                  #If there is at least one in FoV
        avoid_steering = avoid_steering / obs_in_range                #Divide by total in view
        avoid_steering = VectorClass.set_mag(avoid_steering, boid.maxSpeed)
        avoid_steering = avoid_steering - boid.velocity
        avoid_steering = VectorClass.limit(avoid_steering, obs.maxForce)
        
    return avoid_steering
        

##################################
##Defines the edges of the screen
##Params
##boid = A boid from boids class
##################################
def edges(boid):
    if boid.position.x > consts.WIN_WIDTH:
        boid.position.x = 0
    elif boid.position.x < 0:
        boid.position.x = consts.WIN_WIDTH
        
    if boid.position.y > consts.WIN_HEIGHT:
        boid.position.y = 0
    elif boid.position.y < 0:
        boid.position.y = consts.WIN_HEIGHT

##################################
##Drawing function for boids
##Params
##window = Screen object to draw to
##boid = Which boid to draw
##################################
def draw(window, flock_list, obsticle_list):
    for boid in flock_list:
        pg.draw.circle(window, consts.GREEN, (boid.position.x, boid.position.y), 2)
        
    for obs in obsticle_list:
        pg.draw.circle(window, consts.GRAY, (obs.position.x, obs.position.y), obs.size)


##################################
##Update current boid position
##Params
##boid = Which boid to draw
##################################        
def update(flock_list, qTree, obsticle_list):
    for boid in flock_list:
        perception_range = Rectangle(Point(boid.position.x, boid.position.y), 50, 50)        
        found_points = qTree.queryRange(perception_range)
#         radius = min(100, 100)
#         perception_range = Rectangle(Point(boid.position.x, boid.position.y), radius, radius)
#         found_points = qTree.queryRadius(perception_range, Point(boid.position.x, boid.position.y))

        
        temp_align = alignment(boid, found_points, obsticle_list)
        boid.acceleration = boid.acceleration + temp_align
        
        boid.velocity = boid.velocity + boid.acceleration
        boid.position = boid.position + boid.velocity
        boid.acceleration = boid.acceleration * 0
        
        edges(boid)

    
    
    