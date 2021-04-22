import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


'''
vertex = np.array([[1,0,0,bodyRadius*np.cos(np.deg2rad(120))],
				  [0,1,0,bodyRadius*np.sin(np.deg2rad(120))],
				  [0,0,1,coringDepth],
				  [0,0,0,1]])

A = np.array([[1,0,0,0],
			  [0,1,0,0],
			  [0,0,1,coringDepth],
			  [0,0,0,1]])
B = np.array([[1,0,0,0],
			  [0,1,0,0],
			  [0,0,1,0],
			  [0,0,0,1]])

rotateX = np.array([[1,0,0,0],
					[0,np.cos(roll),-np.sin(roll),0],
					[0,np.sin(roll),np.cos(roll),0],
			  		[0,0,0,1]])
rotateY = np.array([[np.cos(pitch),0,np.sin(pitch),0],
					[0,1,0,0],
					[-np.sin(pitch),0,np.cos(pitch),0],
			  		[0,0,0,1]])
rotateZ = np.array([[np.cos(120),-np.sin(120),0,0],
					[np.sin(120),np.cos(120),0,0],
					[0,0,1,0],
			  		[0,0,0,1]])
'''
#C = rotateY.dot(rotateX.dot(A))
#C = rotateZ.matmul(vertex)

#print(C)

def R_Matrix(_matrix):
	return _matrix[0:3,0:3]

def P_Matrix(_matrix):
	return _matrix[0:3,3]

def main():
  print("starting program")


  bodyRadius = 0.5
  coringDepth = 3
  pitch = np.deg2rad(0)
  roll = np.deg2rad(-10)

  bodyCenter = np.array([[1,0,0,bodyRadius],
						[0,1,0,0],
						[0,0,1,coringDepth],
						[0,0,0,1]])
  vertex  = np.array([[1,0,0,bodyRadius],
					[0,1,0,0],
					[0,0,1,coringDepth],
					[0,0,0,1]])
  rotateX = np.array([[1,0,0,0],
					[0,np.cos(roll),-np.sin(roll),0],
					[0,np.sin(roll),np.cos(roll),0],
			  		[0,0,0,1]])
  rotateY = np.array([[np.cos(pitch),0,np.sin(pitch),0],
					[0,1,0,0],
					[-np.sin(pitch),0,np.cos(pitch),0],
			  		[0,0,0,1]])
  rotateZ = np.array([[np.cos(np.deg2rad(120)),-np.sin(np.deg2rad(120)),0,0],
					[np.sin(np.deg2rad(120)),np.cos(np.deg2rad(120)),0,0],
					[0,0,1,0],
			  		[0,0,0,1]])

  fig = plt.figure()
  ax = plt.axes(projection='3d')

  point = P_Matrix(vertex)

  ax.scatter(0,0,0,color='black')
  #ax.scatter(0,0,3,color='blue')
  #ax.scatter(point[0],point[1],point[2],color='black')
  #ax.plot3D([0,point[0]],[0,point[1]],[0,point[2]],linestyle='dashed')

  bodyVertex1 = vertex
  bodyVertex2 = np.matmul(rotateZ,bodyVertex1)
  bodyVertex3 = np.matmul(rotateZ,bodyVertex2)

  bodyVertex1 = np.matmul(rotateX,bodyVertex1)
  bodyVertex2 = np.matmul(rotateX,bodyVertex2)
  bodyVertex3 = np.matmul(rotateX,bodyVertex3)

  bodyVertex1 = np.matmul(rotateY,bodyVertex1)
  bodyVertex2 = np.matmul(rotateY,bodyVertex2)
  bodyVertex3 = np.matmul(rotateY,bodyVertex3)

  bodyVertex = np.concatenate((P_Matrix(bodyVertex1), P_Matrix(bodyVertex2), P_Matrix(bodyVertex3), P_Matrix(bodyVertex1)))
  bodyVertex = np.reshape(bodyVertex,(4,3))

  x,y,z = bodyVertex.T

  ax.add_collection3d(Poly3DCollection([list(zip(x[0:3],y[0:3],z[0:3]))]))
  ax.plot3D(x,y,z,color='black',linewidth=4)
  ax.scatter(x[0:3],y[0:3],z[0:3],color='black')

  ax.set_aspect('equal')
  ax.set_xlim3d(-2,2)
  ax.set_ylim3d(-2,2)
  ax.set_zlim3d(0,4)

  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')

  ax.view_init(azim=-150, elev=30)

  plt.show()





if __name__ == "__main__":
  main()
