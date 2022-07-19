import random
import pygame as pg
import math
import consts

class Point:
    def __init__(self, x, y, randomise=False):
        if randomise:
            self.x = random.randrange(0, 1200)
            self.y = random.randrange(0, 980)
        elif not randomise:
            self.x = x
            self.y = y
        
    def distanceToCentre(self, centre):
        return math.sqrt((centre.x - self.x)**2 + (centre.y - self.y)**2)
 

class Rectangle:
    def __init__(self, centre, width, height):
        self.centre = centre
        self.width = width
        self.height = height
        self.west = self.centre.x - self.width     #West edge of the rectangle
        self.east = self.centre.x + self.width     #East edge
        self.north = self.centre.y - self.height   #North edge
        self.south = self.centre.y + self.height   #South edge
    
    #Checks if rectangle contains a point
    #boid is a Boid object NOT a Point object
    def containsPoint(self, boid):
        return (self.west <= boid.position.x < self.east and
                self.north <= boid.position.y < self.south)
    
    #checks if a range(rectangle/perception range) overlaps a quadtree rectangle
    def intersects(self, _range):
        return not (_range.west > self.east or
                    _range.east < self.west or
                    _range.north > self.south or
                    _range.south < self.north)
    
    #draw function used for drawing Rectangle objects
    def draw(self, rectangle, window):
        left = self.west
        top = self.north
        width = rectangle.width
        height = rectangle.height
        pg.draw.rect(window, consts.WHITE, (left, top, width, height), 1)

#Quadtree Class
class Quadtree:
    def __init__(self, boundary, window, capacity = 4):
        self.boundary = boundary    #Rectangle class for the boundary of a rectangle
        self.capacity = capacity    #The amount of points per area
        self.points = []            #Array to keep the amount of points in this boundary
        self.divided = False        #Flag if this boundary has been divided
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.window = window

        
    def insert(self, point, show_rect):        
        #Check if the point is in the current quadtree
        if not self.boundary.containsPoint(point):
            return False
        
        #Check if the current quadtree is full, if not append to current points
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        #if current QT is full then checks if it has been divided yet
        #If not then divides the QT into smaller squares
        if not self.divided:
            self.divide()
            
            #below used to draw Quadtree rectangles to check if being updated
            if show_rect:
                self.nw.boundary.draw(self.boundary, self.window)
                self.ne.boundary.draw(self.boundary, self.window)
                self.sw.boundary.draw(self.boundary, self.window)
                self.se.boundary.draw(self.boundary, self.window)
        
        #Recursive call to this method
        #After divding, the point is placed into the respective quadrant
        if self.nw.insert(point, show_rect):
            return True
        elif self.ne.insert(point, show_rect):
            return True
        elif self.sw.insert(point, show_rect):
            return True
        elif self.se.insert(point, show_rect):
            return True
        
        return False
    
    #Method that checks if a
    def queryRange(self, _range):
        found_points = []
        
        if not self.boundary.intersects(_range): #enters if False is returned
            return []
        
        for point in self.points:
            if _range.containsPoint(point):
                found_points.append(point)
                
        if self.divided:
            found_points.extend(self.nw.queryRange(_range))
            found_points.extend(self.ne.queryRange(_range))
            found_points.extend(self.sw.queryRange(_range))
            found_points.extend(self.se.queryRange(_range))

        return found_points


    def queryRadius(self, _range, centre):
        found_points = []
        
        if not self.boundary.intersects(_range): #enters if False is returned
            return []
        
        for point in self.points:
            if _range.containsPoint(point) and point.distanceToCentre(centre) <= _range.width:
                found_points.append(point)
                
        if self.divided:
            found_points.extend(self.nw.queryRadius(_range, centre))
            found_points.extend(self.ne.queryRadius(_range, centre))
            found_points.extend(self.sw.queryRadius(_range, centre))
            found_points.extend(self.se.queryRadius(_range, centre))

        return found_points



    def divide(self):
        centre_x = self.boundary.centre.x
        centre_y = self.boundary.centre.y
        new_width = self.boundary.width / 2
        new_height = self.boundary.height / 2
        
        nw = Rectangle(Point(centre_x - new_width, centre_y - new_height), new_width, new_height)
        self.nw = Quadtree(nw, self.window)
        
        ne = Rectangle(Point(centre_x + new_width, centre_y - new_height), new_width, new_height)
        self.ne = Quadtree(ne, self.window)
        
        sw = Rectangle(Point(centre_x - new_width, centre_y + new_height), new_width, new_height)
        self.sw = Quadtree(sw, self.window)
        
        se = Rectangle(Point(centre_x + new_width, centre_y + new_height), new_width, new_height)
        self.se = Quadtree(se, self.window)
        
        self.divided = True


    def __len__(self):
        count = len(self.points)
        if self.divided:
            count+= len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)
            
        return count
    
