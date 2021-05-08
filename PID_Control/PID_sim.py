#from simple_pid import PID
import matplotlib.pyplot as plt
import numpy as np

PVC_length = 0.6096 #2ft in m
motor_speed = 0.03048 #m/s
mu_f = 0.35
lat_earth_p = 1003.853152 #Pa
pipe_d = 0.015875 #m
thrust_f_coeff = 0.18153118262 #lead/2pi*efficiency
lead = 0.005 #m
f_neutral = 33.5810074722

class Motor(object):
	def __init__(self):
   		self.y = 0.0
   		self.v = 0.0
   		self.dt = 0.1
   		self.idx = 0
   		self.friction = 0
	
	def set_y(self, y):
		self.y = y

	def set_dt(self, dt):
		self.dt = dt

	def set_noise(self, distance_noise):
		self.distance_noise = distance_noise

	def move(self, speed, timestep=0.1):
		if speed > motor_speed*2:
			speed = motor_speed*2
		elif speed < -motor_speed*2:
			speed = -motor_speed*2

		depth_percent = self.y/PVC_length
		if depth_percent:
			self.friction = (2*pipe_d*lat_earth_p)*depth_percent
		#print("Friction = " + str(self.friction))

		new_v = self.v + speed
		thrust_f = (new_v/lead)/thrust_f_coeff
		f_sum = thrust_f - self.friction
		f_result = f_sum - f_neutral
		v_final = f_sum*thrust_f_coeff*lead

		self.v = v_final
		self.y += self.v*timestep
		self.idx += 1


def run(motor, p, i, d, setpoint, n=200):
	y_traj = []
	v_traj = []
	e_traj = []
	pos_traj = []
	e_pos = PVC_length - motor.y
	e_prev = setpoint - motor.v
	for i in range(n):
		e = setpoint - motor.v
		dedt = (e - e_prev)/motor.dt
		u = p*e + d*dedt

		motor.move(u)
		e_prev = e
		e_pos = PVC_length - motor.y

		y_traj.append(motor.y)
		v_traj.append(u)
		e_traj.append(e)
		pos_traj.append(e_pos)

		if abs(e_pos) < 0.05:
			print("Stopped at " + str(e_pos))
			break
		elif e_pos < 0.4:
			setpoint = 1
	return (y_traj, v_traj, e_traj, pos_traj)

def get_absmax(data):
	abs_data = map(abs, data)
	maximum = max(abs_data)
	return maximum

def main():
	test = Motor()
	a = run(test, 1, 0, 0, 0.03048, n=250)

	print("y_traj")
	print(a[0])
	print("u")
	print(a[1])
	print("error")
	print(a[2])
	print("position")
	print(a[3])

	b = np.linspace(0, test.dt*250, num=250).tolist()
	b = b[0:len(a[3])]
	plt.plot(b, a[3])
	plt.xlabel("t")
	plt.ylabel("Error")
	plt.title("Velocity Error")
	#plt.xlim(0,25)
	ylim = get_absmax(a[2]) + 2
	plt.ylim(-ylim, ylim)
	plt.show()

if __name__ == "__main__":
	main()