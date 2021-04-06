import numpy as np
import random

from collections import namedtuple
from operator import itemgetter
from pprint import pformat

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# Global Constants
Field_OriginX = 0
Field_OriginY = 0
Field_Width   = 10
Field_Height  = 10

# Named Tuple Container Type Storing Sampling Location Data
SamplingLocation = namedtuple('SamplingLocation',['x','y'])

# Rectangle Node Organizing the Locations Inside the Quad Tree
class RectNode():
  def __init__(self, _x, _y, _w, _h, _locations):
    self.x = _x
    self.y = _y
    self.width = _w
    self.height = _h
    self.locations = _locations
    self.children = []

# Quad Tree Class Used to Efficiently Store Sampling Location Data
class QuadTree():
  def __init__(self, _k, _width, _height, locations):
    self.threshold = _k
    self.samplingLocations = locations
    self.root = RectNode(0, 0, _width, _height, self.samplingLocations)

  def subdivide(self):
    self.recursiveSubdivide(self.root, self.threshold)

  def recursiveSubdivide(self, node, k):
    if len(node.locations)<=k:
      return
    w_ = float(node.width/2)
    h_ = float(node.height/2)

    # South West
    sw_locations = self.contains(node.x, node.y, w_, h_, node.locations)
    sw_node = RectNode(node.x, node.y, w_, h_, sw_locations)
    self.recursiveSubdivide(sw_node, k)
    # North West
    nw_locations = self.contains(node.x, node.y+h_, w_, h_, node.locations)
    nw_node = RectNode(node.x, node.y+h_, w_, h_, nw_locations)
    self.recursiveSubdivide(nw_node, k)
    # North East
    ne_locations = self.contains(node.x+w_, node.y+h_, w_, h_, node.locations)
    ne_node = RectNode(node.x+w_, node.y+h_, w_, h_, ne_locations)
    self.recursiveSubdivide(ne_node, k)
    # South East
    se_locations = self.contains(node.x+w_, node.y, w_, h_, node.locations)
    se_node = RectNode(node.x+w_, node.y, w_, h_, se_locations)
    self.recursiveSubdivide(se_node, k)

    '''
    for location in sw_locations:
      node.locations.remove(location)
    for location in nw_locations:
      node.locations.remove(location)
    for location in ne_locations:
      node.locations.remove(location)
    for location in se_locations:
      node.locations.remove(location)
    '''

    node.children = [sw_node, nw_node, ne_node, se_node]

  def contains(self, _x, _y, _w, _h, _locations):
    result = []
    for location in _locations:
      if location.x >= _x and location.x <= _x+_w and location.y >= _y and location.y <= _y+_h:
        result.append(location)
    return result

  def find_children(self, _node):
    if not _node.children:
      return [_node]
    else:
      children = []
      for child in _node.children:
        children.append(self.find_children(child))
    return children

  #def graph(self):
  #  c = self.find_children(self.root)
  #  print(len(c))

class Field:
  def __init__(self, _count):
    self.sampleCount = _count
    self.samplingNodes = []

    self.samplingNodes = [SamplingLocation(7,2),SamplingLocation(5,4),SamplingLocation(9,6),SamplingLocation(4,7),SamplingLocation(8,1),SamplingLocation(2,3)]
    #self.distributeRandomSamples(0.1)

    self.samplingTree = QuadTree(1, Field_Width, Field_Height, self.samplingNodes)
    self.samplingTree.subdivide()

  def distributeRandomSamples(self, _minSpacing):
    for i in range(self.sampleCount):
      randomNode = Field.SamplingNode(random.random(),random.random())
      self.sampleNodes.append(randomNode)

  def plotNodes(self):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(self.samplingNodes)):
      plt.scatter(self.samplingNodes[i].x, self.samplingNodes[i].y, color=(0,0,1))
    plt.title('Plot Representation of Sampling Field')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.xlim(-0.25,10.25)
    plt.ylim(-0.25,10.25)
    plt.grid()
    ax.set_aspect('equal')
    plt.show()

def main():
  print("starting program")

  samplingField = Field(20)
  #print(samplingField.sampleNodes)
  samplingField.plotNodes()

  #samplingField.samplingTree.graph()

  #samplingField.

if __name__ == "__main__":
  main()