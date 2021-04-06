import numpy as np
import random

from collections import namedtuple
from operator import itemgetter
from pprint import pformat

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

SamplingNode = namedtuple('SamplingNode',['x','y'])

class Field:

  class Node(namedtuple('Node',['location','left_child','right_child'])):
    def __repr__(self):
      return pformat(tuple(self))

  def __init__(self, _count):
    self.sampleCount = _count
    self.samplingNodes = []

    self.samplingNodes = [SamplingNode(7,2),SamplingNode(5,4),SamplingNode(9,6),SamplingNode(4,7),SamplingNode(8,1),SamplingNode(2,3)]
    #self.distributeRandomSamples(0.1)

    self.samplingTree = self.kDTree(self.samplingNodes)

  def distributeRandomSamples(self, _minSpacing):
    for i in range(self.sampleCount):
      randomNode = Field.SamplingNode(random.random(),random.random())
      self.sampleNodes.append(randomNode)

  # K-dimensional Tree used to organizing the 2D points using space-partitioning
  # Allows for quick nearest neighbour search without going through the entire list
  def kDTree(self, _nodeList, depth=0):
    if not _nodeList:
      return None
    k = len(_nodeList[0])
    axis = depth % k
    _nodeList.sort(key=itemgetter(axis))
    median = len(_nodeList) // 2
    return self.Node(
      location    = _nodeList[median],
      left_child  = self.kDTree(_nodeList[:median], depth+1),
      right_child = self.kDTree(_nodeList[median+1:], depth+1))

  '''
  def nearestNeighbourSearch(self, _nodeList, _targetNode, depth=0):
    if not _nodeList:
      return None, float('inf')

    k = len(_nodeList[0])
    axis = depth % k
    depth = 0
  '''

  def plotNodes(self):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(self.samplingNodes)):
      plt.scatter(self.samplingNodes[i].x, self.samplingNodes[i].y, color=(0,0,1))
    plt.title('Plot Representation of Sampling Field')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.xlim(-0.1,1.1)
    plt.ylim(-0.1,1.1)
    plt.grid()
    ax.set_aspect('equal')
    plt.show()

'''
  def bruteForceTSP(self):
    originalNodes = self.sampleNodes
    orderedNodes = [originalNodes[0]]
    originalNodes.pop(0)

  def nearestNeighbourTSP(self):
    originalNodes = self.sampleNodes
    orderedNodes = [originalNodes[0]]
    originalNodes.pop(0)

  def dist(self,_p1,_p2):
    return np.sqrt((_p1[0]-_p2[0])**2+(_p1[1]-_p2[1])**2)
  '''
def main():
  print("starting program")

  #testNode = SampleNode(10,10)
  #print(testNode)

  samplingField = Field(20)
  #print(samplingField.sampleNodes)
  samplingField.plotNodes()
  #samplingField.bruteForceTSP()

if __name__ == "__main__":
  main()