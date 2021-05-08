#from simple_pid import PID
import matplotlib.pyplot as plt
import numpy as np

class Motor(object):
	def __init__(self):
   		self.y = 0.0
   		self.dt = 0.1
   		self.idx = 0
	
	def set_y(self, y):
		self.y = y

	def set_dt(self, dt):
		self.dt = dt

	def set_noise(self, distance_noise):
		self.distance_noise = distance_noise

	def move(self, speed, timestep=0.1):

		if self.idx > 5 and self.idx < 25:
			if speed > 3:
				speed = 3
			elif speed < -3:
				speed = -3
			speed = speed*0.5

		if speed > 3:
			speed = 3
		elif speed < -3:
			speed = -3

		self.y += speed*timestep
		self.idx += 1


def run(motor, p, i, d, setpoint, n=50):
	'''
	x_trajectory, y_trajectory = [], []
	pid = PID(p, i, d, setpoint)

	for i in range(n):
		output = pid(motor.y)
		print(output)
		motor.move(output)
	'''
	y_traj = []
	v_traj = []
	e_traj = []
	e_prev = setpoint - motor.y
	for i in range(n):
		e = setpoint - motor.y
		dedt = (e - e_prev)/motor.dt
		u = p*e + d*dedt
		print(dedt)
		y_traj.append(motor.y)
		v_traj.append(u)
		e_traj.append(e_prev)
		motor.move(u)
		e_prev = e
	return (y_traj, v_traj, e_traj)

def get_absmax(data):
	abs_data = map(abs, data)
	maximum = max(abs_data)
	return maximum

def main():
	test = Motor()
	a = run(test, 10, 0, 0, 5)
	print(a[0])
	print(a[1])
	print(a[2])
	b = np.linspace(0, 5, num=50).tolist()
	plt.plot(b, a[2])
	plt.xlabel("t")
	plt.ylabel("Error")
	plt.title("Positional Error")
	#plt.xlim(0,25)
	ylim = get_absmax(a[2]) + 1
	plt.ylim(-ylim, ylim)
	plt.show()

if __name__ == "__main__":
	main()