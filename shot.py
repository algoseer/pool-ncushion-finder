import numpy as np
from pylab import *

class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y

  def __str__(self):
    return "{}, {}".format(self.x, self.y)

  def __neg__(self):
    return Point(-self.x, -self.y)

  def __add__(self, point):
    return Point(self.x+point.x, self.y+point.y)

  def __sub__(self, point):
    return self + -point

  def __rmul__(self, a):
    return Point(self.x*a, self.y*a)

  def __str__(self):
    return str((self.x, self.y))
   

  #if mx is None then mirror is horizontal else vertical
  def image(self, mx = None, my = None):
    if mx is not None:
        if mx > self.x:
            return Point(self.x + 2*(mx-self.x), self.y)
        else:
            return Point(self.x - 2*(self.x - mx), self.y)
    if my is not None:
        if my > self.y:
            return Point(self.x , self.y + 2*(my-self.y))
        else:
            return Point(self.x, self.y - 2*(self.y - my))

    #Computes cross product between this vector and another (see reference below)
  def det(self, p2):
    return (self.x * p2.y - self.y * p2.x)



'''
Defines a class allowing searching optimal shots with desired number of cushions
between two balls defined by starting position s and target position t
Current version ignores width of the balls or any geometry, also ignores obstacles
'''

class Board:

    def __init__(self, cue1=None, cue2=None, w=100, h=50 ):

        #Define positions of cue1 and cue2 as Point objects
        self.cue1 = cue1
        self.cue2 = cue2

        #define dimensions of boards in the same units
        self.w = w
        self.h = h


    '''
    Estimate a shot when feasible given two shots and a series of edges encoded as L, U, R, D
    Returns: Point on the cushion to hit or None if a shot does not exist
    '''
    def findShot(self, s, t, edge = 'L'):

        if edge == 'L':
            img = s.image(mx = 0)
            p1 = Point(0,0)
            p2 = Point(0,self.h)

        elif edge == 'R':
            img = s.image(mx = self.w)
            p1 = Point(self.w,0)
            p2 = Point(self.w,self.h)

        elif edge == 'U':
            img = s.image(my = self.h)
            p1 = Point(0,self.h)
            p2 = Point(self.w,self.h)

        elif edge == 'D':
            img = s.image(my = 0)
            p1 = Point(0,0)
            p2 = Point(self.w,0)

        #Find the intersection point between this edge and the line joining image and y
        # reference : https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment 

        t = self.intersect(p1, p2, img, t)

        if t>=0 and t<=1:
            return p1 + t*(p2-p1)
        else:
            return None
        
    #Given two lines joining points (p1, p2) and (p3, p4). Find the intercept on the first line where they interesect

    def intersect(self, p1, p2, p3, p4):

        t = (p1-p3).det(p3-p4) / (p1-p2).det(p3-p4)
        return t

    def visualize(self, s=None, t=None, pts=[]):
        
        hlines(0, 0, self.w)
        hlines(self.h, 0, self.w)

        vlines(0, 0, self.h)
        vlines(self.w, 0, self.h)

        if self.cue1:
          plot(self.cue1.x, self.cue1.y,'kX')

        if self.cue2:
          plot(self.cue2.x, self.cue2.y,'kX')

        gca().set_aspect('equal')

        if s is not None:
          c1 = Circle((s.x, s.y), 3,color='r')
          c2 = Circle((t.x, t.y), 3,color='g')

          gca().add_patch(c1)
          gca().add_patch(c2)
      
          pts.insert(0, s)
          pts.append(t)

          x = [p.x for p in pts]
          y = [p.y for p in pts]

          plot(x,y,'-')


        

if __name__ == '__main__':
    #Define a new board
    b = Board()

    b.visualize()
    title('Click yellow ball positions')
    pts = ginput(2)
    

    s = Point(pts[0][0], pts[0][1])
    t = Point(pts[1][0], pts[1][1])

    #s = Point(10,10)
    #t = Point(50,40)

    print(s,t)
    pt  = b.findShot(s,t, edge='D')
    print(s,t,pt)

    #plot this point
    b.visualize(s,t, [pt])
    draw()
    show()
