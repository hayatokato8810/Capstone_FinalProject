import numpy as np
import random

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bridson import poisson_disc_samples

import networkx as nx
#import acopy

class NavigationSystem():
	def __init__(self, _locations, _mx=-1, _my=-1):
		self.sampleNodes = _locations
		print(np.amax(_locations,axis=1))
		self.map_width = _mx
		self.map_height = _my

	def plot(self):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_axisbelow(True)
		plt.title('Plot Representation of Sampling Field')
		plt.xlabel('X (m)')
		plt.ylabel('Y (m)')
		plt.xlim(-0.1*self.map_width,1.1*self.map_width)
		plt.ylim(-0.1*self.map_height,1.1*self.map_height)
		ax.set_aspect('equal')
		plt.grid()
		for node in self.sampleNodes:
			plt.scatter(node[0],node[1],color=(1,0,0),edgecolors = (0,0,0))
		plt.show()

def main():
	print("\nStarting Program...")

	locations = np.array(poisson_disc_samples(20, 20, r=1.2))
	np.random.shuffle(locations)
	print(str(len(locations))+' Samples')

	navigationSystem = NavigationSystem(locations, 20,20)
	navigationSystem.plot()

if __name__ == "__main__":
	main()