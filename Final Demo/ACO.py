import numpy as np
import random

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from itertools import permutations

iteration_count = 2000
#weight_constant = 1.3

class ACO():
	def __init__(self, _basecamp, _locations, _alpha, _beta):
		self.ALPHA = _alpha # Map Scale Constant
		self.BETA  = _beta  # 

		#self.basecamp = _basecamp
		#self.sampleNodes = _locations

		self.sampleNodes = np.insert(_locations, 0, _basecamp, axis=0)

		self.sampleSize = len(self.sampleNodes)
		self.distMatrix = self.computeAllDistance()
		self.pheromone = np.ones((self.sampleSize, self.sampleSize))

		#print(self.generateAnt(0))
		#print(self.generateAnt(0))
		#print(self.generateAnt(0))

		#self.plotPath(self.generateAnt(2))
		#self.plotPath(self.generateAnt(2))

		
		
		#print(bestPath)
		#print(self.evaluatePath(path))
		#self.plotPath(bestPath)
		

		#self.bruteForcePath(0)
		

		#print(self.pheromone)

		'''
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_axisbelow(True)
		plt.plot(progress)
		plt.xlabel('Iterations')
		plt.ylabel('Score')
		plt.show()
		'''


	def computeAllDistance(self):
		matrix = np.zeros((self.sampleSize, self.sampleSize))

		#allNodes = np.insert(self.sampleNodes, 0, self.basecamp, axis=0)


		for index1, node1 in enumerate(self.sampleNodes):
			for index2, node2 in enumerate(self.sampleNodes):
				if index1 > index2:
					dist = np.linalg.norm(node1 - node2)
					matrix[index1, index2] = dist
					matrix[index2, index1] = dist
				elif index1 == index2:
					matrix[index1, index2] = np.inf
		#matrix = 

		return matrix

	def generateAnt(self, _startIndex = -1):
		if _startIndex == -1:
			_startIndex = (int)(random.randint(0,self.sampleSize-1))
		self.pheromone *= 0.99
		distances = np.insert(np.copy(self.distMatrix),0,range(0,self.sampleSize),axis=1)
		pheromones = np.copy(self.pheromone)
		currentIndex = _startIndex
		travelIndex = np.array([currentIndex])
		while len(travelIndex) <= self.sampleSize-1:
			index = (int)(np.where(distances[:,0] == currentIndex)[0])
			bias = pheromones[index,:]

			desirability = pow(self.ALPHA / distances[index,1:], self.BETA)
			desirability *= bias
			desirability /= np.sum(desirability)

			currentIndex = (int)(np.random.choice(distances[:,0],1,p=desirability))

			distances = np.delete(distances, index, 0)
			distances = np.delete(distances, index+1, 1)
			pheromones = np.delete(pheromones, index, 0)
			pheromones = np.delete(pheromones, index, 1)

			travelIndex = np.append(travelIndex,currentIndex)
		score = self.evaluatePath(travelIndex)
		#print(f'score {score}')
		for pos_index in range(len(travelIndex)-1):
			self.pheromone[travelIndex[pos_index], travelIndex[pos_index+1]] += score
		return [travelIndex, score]

	def evaluatePath(self, _pathIndex):
		totalDist = 0
		weightCost = 1
		refScore = 0
		for pos_index in range(len(_pathIndex)-1):
			totalDist += weightCost * self.distMatrix[_pathIndex[pos_index], _pathIndex[pos_index+1]]
			
			# Weight cost function that relates sample count to human effort (modeled exponentially)
			weightCost = pow(self.BETA,pos_index)

		totalDist += weightCost * self.distMatrix[_pathIndex[len(_pathIndex)-1], _pathIndex[0]]
		#refScore += weightCost
		score = (len(_pathIndex) * self.ALPHA) / totalDist
		#refScore = (len(_pathIndex) * self.ALPHA) / refScore
		return score

	def bruteForcePath(self, _startIndex):
		locations = self.sampleNodes.tolist()
		print(locations)
		l = list(permutations(locations))
		maxScore = 0
		bestPath = []
		for i in range(len(l)):
			tempPath = list(l[i])
			tempPath.insert(0,startLocation)

	def computeBestPath(self):
		maxScore = 0
		bestPath = np.array(self.sampleSize)
		progress = []
		
		for iter in range(iteration_count):
			[path,score] = self.generateAnt(0)
			if maxScore < score:
				maxScore = score
				bestPath = path
			progress.append(maxScore)

		#colorScale = np.arange(len(bestPath)-1) / (len(bestPath)-1)

		return maxScore, bestPath#, colorScale

	def plotPath(self, _pathIndex):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_axisbelow(True)
		ax.set_aspect('equal')
		plt.title('Plot Representation of Sampling Field')
		plt.xlabel('X (m)')
		plt.ylabel('Y (m)')
		plt.grid()

		#print(self.sampleSize)
		#print(_pathIndex[:len(_pathIndex)])

		r_color = np.arange(len(_pathIndex)-1) / (len(_pathIndex)-1)
		g_color = 1-np.arange(len(_pathIndex)-1) / (len(_pathIndex)-1)
		
		#plt.arrow(node1[0],node1[1],node2[0]-node1[0],node2[1]-node1[1],width = 0.4,length_includes_head=True, color=(r_color[pos_index],g_color[pos_index],0))

		for pos_index in range(len(_pathIndex)-1):
			node1 = self.sampleNodes[_pathIndex[pos_index]]
			node2 = self.sampleNodes[_pathIndex[pos_index+1]]

			plt.arrow(node1[0],node1[1],node2[0]-node1[0],node2[1]-node1[1],width = 0.4,length_includes_head=True, color=(r_color[pos_index],g_color[pos_index],0))
		
		node1 = self.sampleNodes[_pathIndex[pos_index+1]]
		node2 = self.sampleNodes[_pathIndex[0]]
		plt.arrow(node1[0],node1[1],node2[0]-node1[0],node2[1]-node1[1],width = 0.4,length_includes_head=True, color=(r_color[pos_index],g_color[pos_index],0))


		for node in self.sampleNodes:
			plt.scatter(node[0],node[1],color=(0,0,1),edgecolors=(0,0,0))

		

	#def evalPath(self):