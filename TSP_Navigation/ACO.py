import numpy as np
import random

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bridson import poisson_disc_samples

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
		clusterCount = (int)(np.ceil(float(sampleCount) / sampleCapacity))
		if clusterCount > len(self.colorCode):
			sys.exit('Too many samples / requires more clusters')
		self.clusterCapacity = np.zeros(clusterCount)
		for i in range(clusterCount):
			self.clusterCapacity[i] = (int)(sampleCount // clusterCount)
			if i < sampleCount % clusterCount:
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
			plt.scatter(node[0],node[1],c=self.colorCode[(int)(node[2])],edgecolors = (0,0,0))
		for nodeIndex in range(len(self.clusterCenter)):
			node = self.clusterCenter[nodeIndex]
			plt.scatter(node[0],node[1],200,c=self.colorCode[nodeIndex],marker = '+')
		plt.show()

	def clusterize(self):
		for iter in range(10):

			z = np.zeros((len(self.clusterCapacity),2))
			z_count = np.zeros(len(self.clusterCapacity))
			for node in self.sampleNodes:
				for i in range(len(self.clusterCapacity)):
					if node[2] == i:
						z[i] += node[0:2]
						z_count[i] += 1
			z[:,0] = np.divide(z[:,0],z_count)
			z[:,1] = np.divide(z[:,1],z_count)
			self.clusterCenter = z

			#np.random.shuffle(self.sampleNodes)

			clusterOccupancyCount = np.zeros(len(self.clusterCapacity))
			
			# New Version
			allDistances = np.zeros((len(self.clusterCapacity),len(self.sampleNodes),2))
			for clusterIndex in range(len(self.clusterCapacity)):
				dist = np.zeros((len(self.sampleNodes),2))
				for nodeIndex in range(len(self.sampleNodes)):
					node = self.sampleNodes[nodeIndex,0:2]
					dist[nodeIndex,0] = nodeIndex
					dist[nodeIndex,1] = np.linalg.norm(z[clusterIndex] - node[0:2])
				dist = dist[np.argsort(dist[:,1])]
				allDistances[clusterIndex] = dist
				#for i in range((int)(self.clusterCapacity[clusterIndex])):
				#	print(dist[i,0])
				#print()
			allNodeIndex = np.array(range(len(self.sampleNodes)))
			print(allDistances)
			print(allNodeIndex)


			for i in range(len(self.sampleNodes)):
				for j in range(len(self.clusterCapacity)):
					if clusterOccupancyCount[j] < self.clusterCapacity[j]:
						nodeIndex = (int)(allDistances[j,i,0])
						searchIndex = np.where(nodeIndex == allNodeIndex)
						print("Found at",len(searchIndex[0]))
						if len(searchIndex[0]) == 1:
							self.sampleNodes[nodeIndex,2] = j
							clusterOccupancyCount[j] += 1
							allNodeIndex = np.delete(allNodeIndex,searchIndex)
							
							print(j,nodeIndex)
							print(allNodeIndex)
							print(clusterOccupancyCount)


					#print(allNodeIndex)
						#print(self.sampleNodes)					


			print(self.clusterCapacity)
			# Working Version of Decent Clustering
			'''
			for node in self.sampleNodes:
				dist = np.zeros((len(self.clusterCapacity),2))
				for i in range(len(dist)):
					dist[i,0] = i
					dist[i,1] = np.linalg.norm(z[i] - node[0:2])
				dist = dist[np.argsort(dist[:,1])]
				#print(np.average(dist))
				for i in range(len(dist)):
					index = (int)(dist[i,0])
					print(index)
					if clusterOccupancyCount[index] < self.clusterCapacity[index]:
						node[2] = index
						clusterOccupancyCount[index] += 1
						break
			'''

def main():
	print("starting program")

	locations = np.array(poisson_disc_samples(20, 20, r=1.5))
	np.random.shuffle(locations)
	
	antSystem = ACO(locations,20,20)
	antSystem.plot()
	antSystem.clusterize()
	antSystem.plot()


if __name__ == "__main__":
	main()

