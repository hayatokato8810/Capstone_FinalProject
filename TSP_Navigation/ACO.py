import numpy as np
import random
import math
import time

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bridson import poisson_disc_samples

import acopy
import networkx as nx

# Global Constants
width = 20
height = 20

class ACO():

	colorCode = np.array([(1,0,0),(1,0.5,0),(1,1,0),(0,1,0),(0,1,1),(0,0.5,1),(0,0,1),(0.5,0,1),(1,0,1),(0.5,0.5,0.5),(0,0,0)])
	np.random.shuffle(colorCode)

	def __init__(self, _locations, _x, _y, sampleCapacity = 15):
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

		self.campIndex = 0
		self.path = range(sampleCount)
		self.pheromone = np.zeros((sampleCount,sampleCount))

	def setCamp(self, coord):
		pos = np.delete(self.sampleNodes,2,axis=1)
		idx = np.where((pos == coord).all(axis=1))
		self.campIndex = int(idx[0][0])
		print(self.campIndex)

	def returnCamp(self):
		return self.sampleNodes[self.campIndex]

	def updateSamples(self, location, x, y, sampleCapacity):
		self.__init__(location,x,y,sampleCapacity=sampleCapacity)

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
		for iter in range(100):

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


			#--=====================================================

			clusterOccupancyCount = np.zeros(len(self.clusterCapacity))


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
			while delta[0,2] > 0:
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


			#print(delta)
			
	def compute_aco(self, limit=100):
		solver = acopy.Solver(rho=.03, q=1)
		colony = acopy.Colony(alpha=1, beta=3)
		tours = []
		baseCamp = self.sampleNodes[self.campIndex]
		print(baseCamp)
		baseCampIdx = baseCamp[2]
		baseCamp = baseCamp[:2]

		cluster_nodes = dict.fromkeys(range(self.clusterCount))
		for k, v in cluster_nodes.items():
			if k == baseCampIdx:
				cluster_nodes[k] = []
			else:
				cluster_nodes[k] = [baseCamp]
		for sample in self.sampleNodes:
			cluster_nodes[sample[2]].append(sample[:2])


		for k, v in cluster_nodes.items():
			nodes = cluster_nodes[k]
			G = nx.Graph()
			for idx1, node1 in enumerate(nodes):
				for idx2, node2 in enumerate(nodes):
					x1 = node1[0]
					x2 = node2[0]
					y1 = node1[1]
					y2 = node2[1]
					dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
					G.add_edge(idx1, idx2, weight=dist)

			start_time = time.time()
			tour = solver.solve(G, colony, limit=limit)
			tours.append(tour.path)
			solve_time = time.time() - start_time
			print("--- %s iterations took %s seconds with cost of %s ---" % (limit,round(solve_time,2), round(tour.cost,2)))

		results = []
		for cluster, tour in enumerate(tours):
			nodes = cluster_nodes[cluster]
			result = []
			for idx, pt in enumerate(tour):
				node_to_point = nodes[pt[0]].tolist()
				result.append(tuple(node_to_point + [cluster]))
				if idx + 1 == len(tour):
					node_to_point = nodes[pt[1]].tolist()
					result.append(tuple(node_to_point + [cluster]))
			results.append(result)
		return np.array(results)

				

def main():
	print("starting program")

	locations = np.array(poisson_disc_samples(20, 20, r=2))
	np.random.shuffle(locations)
	
	antSystem = ACO(locations,20,20)
	antSystem.plot()
	print(locations)
	'''
	antSystem = ACO(locations,20,20)
	antSystem.clusterize()
	antSystem.plot()
	path = antSystem.compute_aco()
	path = path.tolist()
	for p in path:
		x,y,c = zip(*p)
		plt.plot(x,y, marker = 'o')
	plt.show()
	'''
	#antSystem.plot()
	#antSystem.clusterize()
	#antSystem.plot()


if __name__ == "__main__":
	main()

