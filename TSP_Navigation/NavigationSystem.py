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
import acopy

import ACO_Matthew as acoM

from itertools import permutations

scale_avg = 5
scale_dis = 0
wcost_avg = 0.9
wcost_dis = 0

class NavigationSystem():

	def __init__(self, _basecamp, _locations, _mx=-1, _my=-1):
		self.basecamp = _basecamp
		self.sampleNodes = _locations
		if _mx == -1 or _my == -1:
			[self.map_width, self.map_height] = np.amax(_locations,axis=0)
		else:
			self.map_width = _mx
			self.map_height = _my

	# Local function for plotting the given set of points
	def plot(self, _locations):

		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_axisbelow(True)
		ax.set_aspect('equal')
		plt.title('Plot Representation of Sampling Field')
		plt.xlabel('X (m)')
		plt.ylabel('Y (m)')
		plt.xlim(-0.1*self.map_width,1.1*self.map_width)
		plt.ylim(-0.1*self.map_height,1.1*self.map_height)
		plt.grid()
		#plt.scatter(self.basecamp[0],self.basecamp[1],color=(1,0,0),edgecolors=(0,0,0))
		for node in _locations:
			plt.scatter(node[0],node[1],color=(0,0,1),edgecolors=(0,0,0))
		for pos_index in range(len(_locations)-1):
			plt.arrow(_locations[pos_index,0],_locations[pos_index,1],_locations[pos_index+1,0]-_locations[pos_index,0],_locations[pos_index+1,1]-_locations[pos_index,1],width = 0.4,length_includes_head=True)
		

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

def main():
	print("\nStarting Program with " + str(len(sys.argv)) + " Arguments")

	# Generate a random user parameter
	scale = random.normalvariate(scale_avg, scale_dis)
	wcost = 0
	while True:
		wcost = random.normalvariate(wcost_avg, wcost_dis)
		if wcost <= 1:
			break

	[locations, scale] = generateLocations(scale)

	print(f'Scale: {scale}')
	print(f'Wcost: {wcost}')
	print(f'Sample Count: {len(locations)}')

	navigationSystem = NavigationSystem(locations[0,:],locations[1:,:],50,50)
	navigationSystem.plot(locations)
	plt.show()
	#[maxScore, bestPath] = navigationSystem.bruteForce(_alpha=scale, _beta=wcost)

	#s = navigationSystem.evaluatePath(locations, _alpha=scale, _beta=wcost)
	#print(f'Score: {s}')
	#print(f'Max Score: {maxScore}')

	#navigationSystem.plot(bestPath)



	antSystem = acoM.ACO(locations,50,50)
	antSystem.clusterize()
	antSystem.plot()
	path = antSystem.compute_aco()
	path = path.tolist()
	for p in path:
		x,y,c = zip(*p)
	#	plt.plot(x,y, marker = 'o')
	#plt.show()

	centerPos = locations[antSystem.campIndex,:]

	navigationSystem = NavigationSystem(locations[0,:],locations[1:,:],50,50)

	totalscore = 0;
	for p in path:
		temp = np.array(p)
		p = np.delete(temp,2,axis=1)
		p = p.tolist()
		p.pop()

		route = np.array(p)
		while route[0].tolist() != centerPos.tolist():
			route = np.roll(route,1)
		route = np.insert(route, len(route), centerPos,0)

		#print(route)

		navigationSystem.plot(route)
		plt.show()

		
		s = navigationSystem.evaluatePath(route)
		totalscore += s
		print(s)
	print('------------------------')
	print(f'total = {totalscore}')
if __name__ == "__main__":
	main()







