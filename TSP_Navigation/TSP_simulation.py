import numpy as np
import random
import math
import time

from collections import namedtuple
from operator import itemgetter
from pprint import pformat

from bridson import poisson_disc_samples

import acopy
import networkx as nx

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Global Constants
Field_OriginX = 0
Field_OriginY = 0
Field_Width   = 10
Field_Height  = 10

c = [(1,0,0),(0,1,0),(0,0,1),(0,0,0),(1,0,1),(0,1,1),(1,1,0)]

coords = []
globalFig = None
globalAx = None
globalField = None
cid = 0

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
    self.clusterCount = 1
    self.assignedCluster = []
    
    location = poisson_disc_samples(width=10, height=10, r=1)
    np.random.shuffle(location)
    print(len(location))

    for i in range(len(location)):
      randomNode = Point(location[i][0],location[i][1])
      self.samplingNodes.append(randomNode)


    self.insertQuad()

    #print(self.samplingTree.points)
    #print(self.samplingTree.child.ne.points)
    #print(self.samplingTree.child.se.points)
    #print(self.samplingTree.child.sw.points)
    #print(self.samplingTree.child.nw.points)

    #print(self.samplingTree.child.se.child)

  def insertQuad(self):
    self.samplingTree = QuadTree(Point(0,0),Point(10,10))
    for node in self.samplingNodes: self.samplingTree.insert(node)

  def kCluster(self, _count):
    self.clusterCount = _count
    sampleCount = len(self.samplingNodes)
    self.assignedCluster = np.random.randint(_count,size=sampleCount)
    print(self.assignedCluster)

    for i in range(10):
      z = []
      for class_index in range(_count):
        cluster = np.where(self.assignedCluster == class_index)[0]
        mX = 0
        mY = 0
        for index in cluster:
          mX = mX + self.samplingNodes[index].x
          mY = mY + self.samplingNodes[index].y
        mX = mX / len(cluster)
        mY = mY / len(cluster)
        z.append(Point(mX,mY))
      for sample_index in range(len(self.samplingNodes)):
        sample = self.samplingNodes[sample_index]
        #print(sample)
        minDist = float('inf')
        for rep_index in range(_count):
          group_rep = z[rep_index]
          D = np.sqrt((group_rep.x - sample.x)*(group_rep.x - sample.x) + (group_rep.y - sample.y)*(group_rep.y - sample.y))
          if minDist > D:
            minDist = D
            self.assignedCluster[sample_index] = rep_index
    print(self.assignedCluster)

  def aco(self, limit=1):
    solver = acopy.Solver(rho=.03, q=1)
    colony = acopy.Colony(alpha=1, beta=3)
    G = nx.Graph()

    for idx1, node1 in enumerate(self.samplingNodes):
      for idx2, node2 in enumerate(self.samplingNodes):
        x1 = node1[0]
        x2 = node2[0]
        y1 = node1[1]
        y2 = node2[1]
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        G.add_edge(idx1, idx2, weight=dist)

    start_time = time.time()
    tour = solver.solve(G, colony, limit=limit)
    solve_time = time.time() - start_time
    print("--- %s iterations took %s seconds with cost of %s ---" % (limit,round(solve_time,2), round(tour.cost,2)))

    #print("START ACO")
    #print(tour.nodes)
    #print(tour.path)
    #print("END ACO")

    result = []
    for idx, pt in enumerate(tour.path):
      result.append(self.samplingNodes[pt[0]])
      if idx + 1 == len(tour.path):
        result.append(self.samplingNodes[pt[1]])
    return result

  def plotNodes(self, _showTree = False, acoPath = None, testing = None):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if testing:
      for i in range(len(self.samplingNodes)):
        plt.scatter(self.samplingNodes[i].x, self.samplingNodes[i].y, color=(0,0,1))
    plt.title('Plot Representation of Sampling Field')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.xlim(-0.25,10.25)
    plt.ylim(-0.25,10.25)
    ax.set_aspect('equal')

    if acoPath:
      if testing:
        iter_num = testing
        fig, axs = plt.subplots(3, 3)
        fig.tight_layout()
        for idx, path in enumerate(acoPath):
          row = idx//3
          col = idx%3
          axs[row,col].set_title(str(iter_num[idx]) + ' Iterations')
          #axs[row,col].set_xlabel('X (m)')
          #axs[row,col].set_ylabel('Y (m)')
          axs[row,col].set_xlim(-0.25,10.25)
          axs[row,col].set_ylim(-0.25,10.25)
          axs[row,col].set_aspect('equal')
          axs[row,col].plot(*zip(*path), marker = 'o')
        plt.show()
      else:
        plt.title('ACO Path Solution of Sampling Field')
        plt.plot(*zip(*acoPath), marker = 'o')
        plt.show()
      return

    for class_index in range(self.clusterCount):
      group = np.where(self.assignedCluster == class_index)[0]
      print(group)
      for i in group:

        plt.scatter(self.samplingNodes[i].x, self.samplingNodes[i].y, color=c[class_index])

    if _showTree:
      self.samplingTree.plot(ax)
    else:
      plt.grid()


    plt.show()

def onclick(event):
  global ix, iy
  global coords
  global globalAx

  ix, iy = event.xdata, event.ydata
  print('x = %d, y = %d'%(ix, iy))

  if ix and iy:
    coords.append(Point(ix, iy))

    globalAx.scatter(*zip(*coords), color=(0,0,1))
    plt.show()

  if len(coords) == 20:
    print(coords)
    globalFig.canvas.mpl_disconnect(cid)
    global globalField
    globalField = Field(20)
    globalField.samplingNodes = coords
    globalField.insertQuad()
    globalField.plotNodes(_showTree=True, testing=True)
    coords = []
    plt.close(globalFig)

  return coords

def emptyPlot():
  global globalFig
  globalFig = plt.figure()
  global globalAx
  globalAx = globalFig.add_subplot(111)
  plt.xlim(-0.25,10.25)
  plt.ylim(-0.25,10.25)
  plt.title("Select 20 points")
  globalAx.plot()

  global cid
  cid = globalFig.canvas.mpl_connect('button_press_event', onclick)
  plt.show()

def get_globalField():
  return globalField

def main():
  print("starting program")

  #samplingField = Field(20)
  emptyPlot()
  #samplingField.samplingNodes = [(0.5131056798669771, 0.189988713306955), (4.424680382500854, 0.23245640554668934), (7.483040641931, 0.0946238632236509), (1.8606118342652715, 0.766060487728716), (6.257158323659654, 0.986532689453962), (0.6497661227851843, 1.659320571614563), (3.0474567475569545, 1.828477470184365), (5.421975603438306, 1.7754921958946748), (7.4808293389415415, 1.986726966448749), (8.509483193382506, 1.4490188354311915), (0.0634679531576543, 2.6347865804033175), (1.7724831159035581, 2.451870667522988), (9.958286495576061, 2.7976886124615605), (2.770813523641103, 3.5302246878506858), (4.0000697227335476, 3.2382173028594026), (5.818643785541418, 3.3106038075324022), (7.001644357811106, 2.964307447418969), (8.28588116561309, 3.1499990602392423), (0.7186139189407335, 3.5947924446732813), (1.8985343684040883, 4.069567709570926), (7.9248086346724085, 4.14734739932317), (0.33423603515145217, 4.83021996808751), (3.4261617333137417, 4.53011352610069), (5.393569841329768, 4.777079692484352), (8.762796661960854, 4.717445033078811), (3.586992775879593, 5.561545562448422), (6.370343180968799, 5.08121962669655), (1.0046001092387147, 5.918642589578775), (2.3194077022614996, 5.873534971589171), (5.310402529441646, 6.004211495244074), (8.456157236031007, 5.889281145246091), (2.3801605330354314, 6.941999727982097), (6.268972455012896, 6.6637731787384045), (1.0909827025791494, 7.268333144368183), (3.669125093444218, 7.580526112384653), (4.861157853640513, 7.106190348310623), (7.245937813960419, 7.178773753230456), (0.3207156196358927, 8.124266174607374), (6.517160335892738, 7.996864140048311), (8.477549702453208, 7.885493670252149), (2.415188783152793, 8.549679969615786), (4.065081124044053, 8.531511376281635), (5.441040733911133, 9.0766946299141), (9.963865003363756, 8.80306841907342), (4.648970029443678, 9.786484801970843), (6.810362191264805, 9.579257026581413), (8.270320244060807, 9.573189116397906), (3.647256667469297, 9.899845438489988)]
  #path_1 = samplingField.aco(limit=1)
  #path_10 = samplingField.aco(limit=10)
  #path_25 = samplingField.aco(limit=25)
  #path_50 = samplingField.aco(limit=50)
  #path_100 = samplingField.aco(limit=100)
  #ath_150 = samplingField.aco(limit=150)
  #path_200 = samplingField.aco(limit=200)
  #path_250 = samplingField.aco(limit=250)
  #path_300 = samplingField.aco(limit=300)
  #print(samplingField.sampleNodes)
  #samplingField.plotNodes(True)
  #samplingField.kCluster(5)

  #samplingField.plotNodes(acoPath = [path_1,path_10,path_25,path_50,path_100,path_150,path_200,path_250,path_300], testing=[1,10,25,50,100,150,200,250,300])
  #samplingField.plotNodes()

  #samplingField.samplingTree.graph()

  #samplingField.

if __name__ == "__main__":
  main()