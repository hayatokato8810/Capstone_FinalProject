import numpy as np
import random

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bridson import poisson_disc_samples

import networkx as nx

import sys, argparse
import json

import ACO as aco
import Clustering as cluster

from itertools import permutations

scale_avg = 5
scale_dis = 0
wcost_avg = 1.1
wcost_dis = 0

class NavigationSystem():

	def __init__(self, _basecamp, _locations, _mx=-1, _my=-1, _alpha=1, _beta=1):
		self.basecamp = _basecamp
		self.sampleNodes = _locations
		if _mx == -1 or _my == -1:
			[self.map_width, self.map_height] = np.amax(_locations,axis=0)
		else:
			self.map_width = _mx
			self.map_height = _my

		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_axisbelow(True)
		ax.set_aspect('equal')
		plt.title('Plot Representation of Sampling Field')
		plt.xlabel('X (m)')
		plt.ylabel('Y (m)')
		plt.xlim([0,self.map_width])
		plt.ylim([0,self.map_height])
		plt.grid()
		plt.scatter(self.basecamp[0],self.basecamp[1],color=(1,0,0),edgecolors=(0,0,0))
		for node in self.sampleNodes:
			plt.scatter(node[0],node[1],color=(0,0,1),edgecolors=(0,0,0))
		plt.show()


		print(f'Sample Count: {len(self.sampleNodes)}')



		self.Cluster = cluster.Clustering(_locations, _alpha, _beta, 10)
		self.sortedLocation = self.Cluster.sampleNodes



		trajectory = np.empty((1,2))
		for clusterID in range(self.Cluster.clusterCount):
			clusterLocations = []
			for node in self.sortedLocation:
				if node[2] == clusterID:
					clusterLocations.append(node[0:2].tolist())
			acoSystem = aco.ACO(self.basecamp, np.array(clusterLocations), _alpha, _beta, 0)
			result = acoSystem.computeBestPath() 

			#print(result[0])

			clusterLocations = np.insert(clusterLocations, 0, self.basecamp, axis=0)

			print(result[1])
			print(len(clusterLocations))

			fig = plt.figure()
			ax = fig.add_subplot(111)
			ax.set_axisbelow(True)
			ax.set_aspect('equal')
			plt.title('Plot Representation of Sampling Field')
			plt.xlabel('X (m)')
			plt.ylabel('Y (m)')
			plt.xlim([0,self.map_width])
			plt.ylim([0,self.map_height])
			plt.grid()

			colorScale = np.arange(len(result[1])) / (len(result[1]))

			for index in range(len(result[1])-1):
				#pathID = result[1][index]
				#print(result[1][index])

				pathID1 = result[1][index]
				pathID2 = result[1][index+1]
				#print(clusterLocations[result[1][pathID],:])
				node1 = clusterLocations[pathID1]
				node2 = clusterLocations[pathID2]
				plt.arrow(node1[0],node1[1],node2[0]-node1[0],node2[1]-node1[1],width = 0.4,length_includes_head=True, color=(colorScale[index],1-colorScale[index],0))
			node1 = clusterLocations[pathID2]
			node2 = clusterLocations[0]
			plt.arrow(node1[0],node1[1],node2[0]-node1[0],node2[1]-node1[1],width = 0.4,length_includes_head=True, color=(colorScale[index+1],1-colorScale[index+1],0))

			trajectory = np.append(trajectory, clusterLocations, axis=0)

				#print(clusterLocations[pathID])
			#print(clusterLocations)

			plt.show()

		print(trajectory)
		print(len(trajectory))



		




		

	#def computeBestPath(self):

	# alpha determines power of the fraction (a > 0)
	def evaluatePath(self, _locations, _alpha=1, _beta=1):
		score = 0
		multiplier = 1
		for index in range(len(_locations)-1):
			dist = np.linalg.norm(_locations[index] - _locations[index+1])
			score += multiplier * np.exp(-dist/_alpha)
			multiplier *= _beta
		return score

	def bruteForce(self, _alpha, _beta):
		startLocation = self.basecamp.tolist()
		locations = self.sampleNodes.tolist()
		print(len(locations))
		l = list(permutations(locations))
		maxScore = 0
		bestPath = []
		for i in range(len(l)):
			tempPath = list(l[i])
			tempPath.insert(0,startLocation)
			score = self.evaluatePath(np.array(tempPath), _alpha, _beta)
			if maxScore < score:
				maxScore = score
				bestPath = np.array(tempPath)

		return [maxScore, bestPath]

def generateLocations(_scale):
	# No argument given
	if len(sys.argv[1:]) == 0:
		print('Generate locations...')
		while True:
			nodes = np.array(poisson_disc_samples(50, 50, r=_scale))
			if len(nodes) > 2:
				break
		np.random.shuffle(nodes)
		data = {}
		data['location'] = nodes.tolist()
		data['scale'] = _scale
	# Save or load with given filename
	elif len(sys.argv[1:]) == 2:
		filename = sys.argv[2]
		# Save JSON File
		if sys.argv[1] == '-s':
			print('Saving location file...')
			while True:
				nodes = np.array(poisson_disc_samples(50, 50, r=_scale))
				if len(nodes) > 2:
					break
			np.random.shuffle(nodes)
			data = {}
			data['location'] = nodes.tolist()
			data['scale'] = _scale
			with open(filename,'w') as outfile:
				json.dump(data, outfile)
		# Load JSON File
		elif sys.argv[1] == '-l':
			print('Loading location file...')
			with open(filename) as json_file:
				data = json.load(json_file)
	return [np.array(data['location']), data['scale']]

#def sortDistance(_refLocation, _otherLocations):
#	print(np.where(_otherLocations == _refLocation))

# Local function for plotting the given set of points
def plot(_locations):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_axisbelow(True)
	ax.set_aspect('equal')
	plt.title('Plot Representation of Sampling Field')
	plt.xlabel('X (m)')
	plt.ylabel('Y (m)')
	#plt.xlim(-0.1*self.map_width,1.1*self.map_width)
	#plt.ylim(-0.1*self.map_height,1.1*self.map_height)
	plt.grid()
	#plt.scatter(self.basecamp[0],self.basecamp[1],color=(1,0,0),edgecolors=(0,0,0))
	for node in _locations:
		plt.scatter(node[0],node[1],color=(0,0,1),edgecolors=(0,0,0))
	for pos_index in range(len(_locations)-1):
		plt.arrow(_locations[pos_index,0],_locations[pos_index,1],_locations[pos_index+1,0]-_locations[pos_index,0],_locations[pos_index+1,1]-_locations[pos_index,1],width = 0.4,length_includes_head=True)
	plt.show()

def main():
	print("\nStarting Program with " + str(len(sys.argv)) + " Arguments")

	# Generate a random user parameter
	scale = random.normalvariate(scale_avg, scale_dis)
	wcost = 0
	while True:
		wcost = random.normalvariate(wcost_avg, wcost_dis)
		if wcost <= wcost_avg:
			break

	# Generate a random samo=pling location
	[locations, scale] = generateLocations(scale)

	#print(f'Scale: {scale}')
	#print(f'Wcost: {wcost}')
	#print(f'Sample Count: {len(locations)}')

	#print(locations)

	basecamp = locations[0,:]
	locations = locations[1:,:]

	#print(locations)
	#print(basecamp)

	navigationSystem = NavigationSystem(basecamp, locations,50,50, _alpha=scale, _beta=wcost)
	#plot(locations)






if __name__ == "__main__":
	main()







