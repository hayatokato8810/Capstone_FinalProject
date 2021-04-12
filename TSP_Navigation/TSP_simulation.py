import numpy as np
import random

from collections import namedtuple
from operator import itemgetter
from pprint import pformat

from bridson import poisson_disc_samples

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Global Constants
Field_OriginX = 0
Field_OriginY = 0
Field_Width   = 10
Field_Height  = 10

# Named Tuple Container Class Storing Sampling Location Data
class Point(namedtuple('Point',['x','y'])):
  def __repr__(self):
    return pformat(tuple(self))

# Quad Tree Class Used to Efficiently Store Sampling Location Data
class QuadTree():

  Child = namedtuple('Child',['ne','se','sw','nw'])

  def __init__(self, _bottomLeft=Point(0,0), _topRight=Point(0,0), _n=1):
    self.points = []
    self.bottomLeft = _bottomLeft
    self.topRight = _topRight
    self.threshold = _n
    self.child = None

  def insert(self, _point):
    if not self.inBoundary(_point):
      return False
    if len(self.points) < self.threshold and not self.child:
      self.points.append(_point)
      return True
    if not self.child: # Subdivide
      center = Point(0.5*(self.topRight.x + self.bottomLeft.x), 0.5*(self.topRight.y + self.bottomLeft.y))
      self.child = self.Child(
        QuadTree(center, self.topRight), # NE
        QuadTree(Point(center.x, self.bottomLeft.y), Point(self.topRight.x, center.y)), # SE
        QuadTree(self.bottomLeft, center),
        QuadTree(Point(self.bottomLeft.x, center.y), Point(center.x, self.topRight.y)))
    for index in range(4):
      if self.child[index].insert(_point):
        return True
    return False

  def inBoundary(self, _p):
    return _p.x <= self.topRight.x and _p.x >= self.bottomLeft.x and _p.y <= self.topRight.y and _p.y >= self.bottomLeft.y

  def plot(self, _axis):
    _axis.add_patch(Rectangle((self.bottomLeft.x,self.bottomLeft.y),self.topRight.x - self.bottomLeft.x,self.topRight.y - self.bottomLeft.y,fill=False))
    if self.child:
      for index in range(4):
        self.child[index].plot(_axis)

class Field:
  def __init__(self, _count):
    self.sampleCount = _count
    self.samplingNodes = []#[Point(7,2),Point(9,6),Point(4,7),Point(8,1),Point(2,3),Point(5,4)]

    location = poisson_disc_samples(width=10, height=10, r=1)
    print(len(location))
    for i in range(len(location)):
      randomNode = Point(location[i][0],location[i][1])
      self.samplingNodes.append(randomNode)

    self.samplingTree = QuadTree(Point(0,0),Point(10,10))
    for node in self.samplingNodes: self.samplingTree.insert(node)

    #print(self.samplingTree.points)
    #print(self.samplingTree.child.ne.points)
    #print(self.samplingTree.child.se.points)
    #print(self.samplingTree.child.sw.points)
    #print(self.samplingTree.child.nw.points)

    #print(self.samplingTree.child.se.child)

  def plotNodes(self, _showTree = False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(self.samplingNodes)):
      plt.scatter(self.samplingNodes[i].x, self.samplingNodes[i].y, color=(0,0,1))
    plt.title('Plot Representation of Sampling Field')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.xlim(-0.25,10.25)
    plt.ylim(-0.25,10.25)
    #plt.grid()
    ax.set_aspect('equal')

    if _showTree: self.samplingTree.plot(ax)

    plt.show()


def main():
  print("starting program")

  samplingField = Field(20)
  #print(samplingField.sampleNodes)
  samplingField.plotNodes(True)


  #samplingField.samplingTree.graph()

  #samplingField.

if __name__ == "__main__":
  main()