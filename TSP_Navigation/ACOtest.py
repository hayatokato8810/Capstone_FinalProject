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

# Constants
width = 20
height = 20

user_weight = 150 #lb
vaporationRate = 0.1

def main():
  print("starting program")
  location = np.array(poisson_disc_samples(width, height, r=2))
  np.random.shuffle(location)

  plotPath(location)

  print(evaluatePath(location))

  newLocation = generateSingleAgent(location)
  plotPath(newLocation)


  print(evaluatePath(newLocation))

  #print(location)

def plotPath(locations):
  fig = plt.figure()
  ax = fig.add_subplot(111)
  plt.title('Plot Representation of Sampling Field')
  plt.xlabel('X (m)')
  plt.ylabel('Y (m)')
  plt.xlim(0,width)
  plt.ylim(0,height)
  ax.set_aspect('equal')
  plt.grid()
  for position in locations:
    plt.scatter(position[0],position[1])
  for pos_index in range(len(locations)-1):
	  plt.arrow(locations[pos_index,0],locations[pos_index,1],locations[pos_index+1,0]-locations[pos_index,0],locations[pos_index+1,1]-locations[pos_index,1],width = 0.2,length_includes_head=True)
  plt.show()

def generateSingleAgent(location):
  travelLocation = np.copy(location)
  travelIndex = np.random.randint(len(travelLocation))
  reachedLocation = travelLocation[travelIndex]
  while len(travelLocation) > 1:
    currentLocation = travelLocation[travelIndex]
    travelLocation = np.delete(travelLocation,travelIndex,axis=0)
    desirability = np.zeros(len(travelLocation))
    for i in range(len(travelLocation)):
      dist = np.linalg.norm(currentLocation - travelLocation[i])
      desirability[i] = pow(1/dist,10)
    desirability = desirability/np.sum(desirability)
    travelIndex = (int)(np.random.choice(range(len(travelLocation)),1,p=desirability))
    reachedLocation = np.append(reachedLocation,travelLocation[travelIndex])
  reachedLocation = np.reshape(reachedLocation,(len(reachedLocation)/2,2))
  return reachedLocation

def evaluatePath(path):
  cost = 0
  for i in range(len(path)-1):
    dist = np.linalg.norm(path[i] - path[i+1])
    cost = cost + dist*1
  return cost

#def getPath():


if __name__ == "__main__":
  main()