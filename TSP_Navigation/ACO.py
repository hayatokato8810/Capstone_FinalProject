import numpy as np
import random

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

<<<<<<< HEAD
from bridson import poisson_disc_samples

import networkx as nx

# Global Constants
width = 20
height = 20
sampleCapacity = 20

class ACO():

	colorCode = np.array([(1,0,0),(1,0.5,0),(1,1,0),(0,1,0),(0,1,1),(0,0.5,1),(0,0,1),(0.5,0,1),(1,0,1),(0.5,0.5,0.5),(0,0,0)])
	np.random.shuffle(colorCode)

	def __init__(self, _locations, _x, _y):
		self.width = _x
		self.height = _y

		sampleCount = len(_locations)

		# Compute the ideal capacity per cluster to equalize the number of samples per expedition
		self.clusterCount = (int)(np.ceil(float(sampleCount) / sampleCapacity))
		if self.clusterCount > len(self.colorCode):
			sys.exit('Too many samples / requires more clusters')
		self.clusterCapacity = np.zeros(self.clusterCount)
		for i in range(self.clusterCount):
			self.clusterCapacity[i] = (int)(sampleCount // self.clusterCount)
			if i < sampleCount % self.clusterCount:
				self.clusterCapacity[i] += 1

		print(self.clusterCapacity)

		clusterID = np.zeros(sampleCount)
		i = 0
		for j in range(len(self.clusterCapacity)):
			for k in range((int)(self.clusterCapacity[j])):
				clusterID[i] = j
				i += 1
		clusterID = np.array([clusterID.tolist()])
		np.random.shuffle(clusterID)

		# First two columns are location coordinates, third column is cluster ID
		self.sampleNodes = np.concatenate((_locations,clusterID.T),axis=1)
		self.clusterCenter = np.zeros((len(self.clusterCapacity),2))

		self.path = range(sampleCount)
		self.pheromone = np.zeros((sampleCount,sampleCount))

	def plot(self):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_axisbelow(True)
		plt.title('Plot Representation of Sampling Field')
		plt.xlabel('X (m)')
		plt.ylabel('Y (m)')
		plt.xlim(-0.1*self.width,1.1*self.width)
		plt.ylim(-0.1*self.width,1.1*self.height)
		ax.set_aspect('equal')
		plt.grid()
		for node in self.sampleNodes:
			plt.scatter(node[0],node[1],color=self.colorCode[(int)(node[2])],edgecolors = (0,0,0))
		for nodeIndex in range(len(self.clusterCenter)):
			node = self.clusterCenter[nodeIndex]
			plt.scatter(node[0],node[1],200,color=self.colorCode[nodeIndex],marker = '+')
		plt.show()

	def clusterize(self):
		for iter in range(1000):
			print(iter)

			# Compute Center Nodes
			center_node = np.zeros((len(self.clusterCapacity),2))
			z_count = np.zeros(len(self.clusterCapacity))
			for node in self.sampleNodes:
				for i in range(len(self.clusterCapacity)):
					if node[2] == i:
						center_node[i] += node[0:2]
						z_count[i] += 1
			center_node[:,0] = np.divide(center_node[:,0],z_count)
			center_node[:,1] = np.divide(center_node[:,1],z_count)
			self.clusterCenter = center_node

			#np.random.shuffle(self.sampleNodes)

			clusterOccupancyCount = np.zeros(len(self.clusterCapacity))

			# Compute Delta for each Element
			delta = np.zeros((len(self.sampleNodes),3))
			for nodeIndex in range(len(self.sampleNodes)):
				node = self.sampleNodes[nodeIndex,:]
				currentID = (int)(node[2])
				currentDist = np.linalg.norm(center_node[currentID] - node[0:2])
				maxDelta = -np.inf
				maxDeltaID = currentID
				for clusterID in range(self.clusterCount):
					# (Positive means improvement)
					temp_delta = currentDist - np.linalg.norm(center_node[clusterID] - node[0:2])
					if maxDelta < temp_delta and temp_delta != 0:
						maxDelta = temp_delta
						maxDeltaID = clusterID
				delta[nodeIndex,0] = nodeIndex
				delta[nodeIndex,1] = maxDeltaID
				delta[nodeIndex,2] = maxDelta
			delta = delta[np.argsort(delta[:,2])[::-1]]

			#print(len(delta))
			while len(delta) > 0 and delta[0,2] > 0:
				#print('delta',delta[0,2])
				#for j in range(len(delta)):
				j = 0
				while j < len(delta):
					#print('j',j)
					#print('sampleID',delta[j,0])
					#print('clusterID',self.sampleNodes[(int)(delta[j,0]),2])
					clusterID = self.sampleNodes[(int)(delta[j,0]),2]


					if clusterID == delta[0,1]:
						if delta[0,2] > abs(delta[j,2]): # if it results in improvement
							firstID = (int)(delta[0,0])
							secondID = (int)(delta[j,0])
							#print('swap',clusterID,firstID,self.sampleNodes[firstID,2], secondID,self.sampleNodes[secondID,2])


							self.sampleNodes[secondID,2] = self.sampleNodes[firstID,2]
							self.sampleNodes[firstID,2] = clusterID
							delta = np.delete(delta,[j],axis=0)
							#print(delta)
					j += 1

				delta = np.delete(delta,[0],axis=0)




				#print(delta[i,2])
				#i += 1




			#print(delta)
			

def main():
	print("starting program")

	locations = np.array(poisson_disc_samples(20, 20, r=1.2))
	np.random.shuffle(locations)
	print(len(locations))
	
	antSystem = ACO(locations,20,20)
	antSystem.plot()
	antSystem.clusterize()
	antSystem.plot()


if __name__ == "__main__":
	main()
=======
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


>>>>>>> 4c84c4b89eb8456270224dfe7f0a3e2eb9c6a5c5

