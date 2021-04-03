import numpy as np
import random
import matplotlib.pyplot as plt

class Field:
  
  def __init__(self,_count):
    self.sampleCount = _count
    self.sampleNodes = []
    for i in range(self.sampleCount):
      randomNode = (random.random(),random.random())
      self.sampleNodes.append(randomNode)

  def plotNodes(self):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(self.sampleCount):
      plt.scatter(self.sampleNodes[i][0],self.sampleNodes[i][1],color=(0,0,1))
    plt.title('Plot Representation of Sampling Field')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.xlim(-0.1,1.1)
    plt.ylim(-0.1,1.1)
    plt.grid()
    ax.set_aspect('equal')
    plt.show()

  def bruteForceTSP(self):
    originalNodes = self.sampleNodes
    orderedNodes = [originalNodes[0]]
    originalNodes.pop(0)

  def nearestNeighborTSP(self):
    originalNodes = self.sampleNodes
    orderedNodes = [originalNodes[0]]
    originalNodes.pop(0)

  def dist(self,_p1,_p2):
    return np.sqrt((_p1[0]-_p2[0])**2+(_p1[1]-_p2[1])**2)

def main():
  samplingField = Field(20)
  samplingField.plotNodes()
  samplingField.bruteForceTSP()

if __name__ == "__main__":
  main()