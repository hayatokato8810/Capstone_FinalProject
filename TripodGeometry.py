import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Tripod():
	LEG_COUNT = 3
	def __init__(self, _radius, _angle, _minLen, _maxLen):
		self.bodyRadius = _radius
		self.legAngle = np.deg2rad(_angle)
		self.maxLength = _maxLen
		self.minLength = _minLen

		self.leg = [self.maxLength]*self.LEG_COUNT

	def plot(self, _axis):
		# Main Body
		index = np.arange(0,self.LEG_COUNT+1)
		x = list(self.bodyRadius*np.sin(np.deg2rad(360/self.LEG_COUNT*index)))
		y = list(self.bodyRadius*np.cos(np.deg2rad(360/self.LEG_COUNT*index)))
		z = [0]*(self.LEG_COUNT+1)
		_axis.add_collection3d(Poly3DCollection([list(zip(x,y,np.zeros(3)))]))
		_axis.plot3D(x,y,z,'black')

		# Tripod Legs
		lx = [0]*self.LEG_COUNT
		ly = [0]*self.LEG_COUNT
		lz = [0]*self.LEG_COUNT
		for i in range(self.LEG_COUNT):
			lx[i] = (self.bodyRadius+self.leg[i]*np.sin(self.legAngle))*np.sin(np.deg2rad(360/self.LEG_COUNT*i))
			ly[i] = (self.bodyRadius+self.leg[i]*np.sin(self.legAngle))*np.cos(np.deg2rad(360/self.LEG_COUNT*i))
			lz[i] = -self.leg[i]*np.cos(self.legAngle)
			_axis.plot3D([x[i],lx[i]],[y[i],ly[i]],[z[i],lz[i]],'black')

		# Ground Plane
		gridRes = 30
		x0, x1, x2 = lx
		y0, y1, y2 = ly
		z0, z1, z2 = lz
		ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
		vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]
		u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]
		point  = np.array([x0,y0,z0])
		normal = np.array(u_cross_v)
		d = -point.dot(normal)
		xx, yy = np.meshgrid(np.linspace(-2,2,gridRes), np.linspace(-2,2,gridRes))
		z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]
		_axis.plot_wireframe(xx, yy, z)

		# Plot Formatting
		_axis.set_aspect('equal')
		_axis.set_xlim3d(-2,2)
		_axis.set_ylim3d(-2,2)
		_axis.set_zlim3d(-3,1)
		_axis.view_init(azim=-50, elev=20)

def main():
  print("starting program")

  fig = plt.figure()
  ax = plt.axes(projection='3d')

  robotLeg = Tripod(0.2,25,0,2.5)
  robotLeg.leg[0] = 2
  robotLeg.leg[1] = 2.4
  robotLeg.leg[2] = 2.2
  robotLeg.plot(ax)

  plt.show()

if __name__ == "__main__":
  main()
