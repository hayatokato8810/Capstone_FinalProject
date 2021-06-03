from tkinter import *
from ACO import *

import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from bridson import poisson_disc_samples

class NavUI:
	def __init__(self):
		self.coords = []
		self.ax = None
		self.fig = None
		self.canvas = None
		self.cid = None
		self.field = None
		self.path = None
		self.base_root = None
		self.empty_root = None
		self.node_idx = 0
		self.demo_fig = None
		self.demo_ax = None
		self.demo_canvas = None
		self.demo_pos = None
		self.ani_x = []
		self.ani_y = []

		self.root = Tk()
		self.root.wm_title("Navigation")  
		self.root.geometry('400x200')

		self.setting_lbl = Label(self.root, text="Settings")
		self.setting_lbl.grid(column=0, row=0, columnspan = 2) 
		self.setting_update = Button(self.root, text="Update", command=self.update_settings)
		self.setting_update.grid(column=0, row=1, columnspan = 2)

		self.max_cluster_lbl = Label(self.root, text="Max # of samples/trip")
		self.max_cluster_lbl.grid(column=0, row=2) 
		self.max_cluster_ent = Entry(self.root, width = 10)
		self.max_cluster_ent.grid(column=1, row=2)

		self.field_lbl = Label(self.root, text="Field dimensions")
		self.field_lbl.grid(column=0, row=3, columnspan = 2) 
		self.field_x_lbl = Label(self.root, text="X")
		self.field_x_lbl.grid(column=0, row=4)
		self.field_x_ent = Entry(self.root, width=10)
		self.field_x_ent.grid(column=1, row=4)
		self.field_y_lbl = Label(self.root, text="Y")
		self.field_y_lbl.grid(column=0, row=5)
		self.field_y_ent = Entry(self.root, width=10)
		self.field_y_ent.grid(column=1, row=5)

		self.node_num_lbl = Label(self.root, text="Total # of samples")
		self.node_num_lbl.grid(column=0, row=6)
		self.node_num_ent = Entry(self.root, width=10)
		self.node_num_ent.grid(column=1, row=6)

		self.node_select = Button(self.root, text="Node Selection", command=self.emptyPlot, width = 20)
		self.node_select.grid(column=3, row=0, columnspan = 2)

		self.node_gen = Button(self.root, text="Random Node Generation", command=self.generate_nodes, width = 20)
		self.node_gen.grid(column=3, row=1, columnspan = 2)

		self.base_select = Button(self.root, text="Base Selection", command=self.select_base, width = 20)
		self.base_select.grid(column=3, row=2, columnspan = 2)

		self.aco_btn = Button(self.root, text="ACO Solve", command=self.aco_solve, width = 20)
		self.aco_btn.grid(column=3, row=3, columnspan = 2)

		#self.demo = Button(self.root, text="Demo", command=self.test_ani, width = 20)
		self.demo = Button(self.root, text="Demo", command=self.demo, width = 20)
		self.demo.grid(column=3, row=4, columnspan = 2)

		self.field = None
		self.n_sample_carry = 5
		self.n_nodes = 20
		self.x = 20
		self.y = 20
		self.base = None

	def windowMsg(self,msg):
		confirm = Tk()
		text = Label(confirm, text=msg)
		text.pack(side="top", fill="x", pady=10)
		ok = Button(confirm, text="Okay", command=confirm.destroy)
		ok.pack()
		confirm.mainloop()

	def update_settings(self):
		self.n_sample_carry = int(self.max_cluster_ent.get())
		self.x = float(self.field_x_ent.get())
		self.y = float(self.field_y_ent.get())
		self.n_nodes = int(self.node_num_ent.get())
		
		self.windowMsg("Settings updated.")

	def generate_nodes(self):
		self.base = None
		coords = poisson_disc_samples(self.x, self.y, r=2)
		self.coords = coords
		locations = np.array(coords)
		np.random.shuffle(locations)
		self.field = ACO(locations, self.x, self.y, sampleCapacity = self.n_sample_carry)

		self.windowMsg("Generated nodes.")

	def emptyPlot(self):
		self.base = None
		self.empty_root = Tk()

		self.coords = []
		self.fig = plt.figure()
		self.canvas = FigureCanvasTkAgg(self.fig, master = self.empty_root)
		self.ax = self.fig.add_subplot(111)
		self.ax.set_xlim(-0.1*self.x,1.1*self.x)
		self.ax.set_ylim(-0.1*self.y,1.1*self.y)
		self.ax.set_title("Select " + str(self.n_nodes) + " points")
		self.ax.set_aspect('equal')
		plt.grid()
		self.ax.plot()

		self.cid = self.canvas.mpl_connect('button_press_event', self.onclick)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	def select_base(self):
		if self.field:
			self.base_root = Tk()

			self.fig = plt.figure()
			self.canvas = FigureCanvasTkAgg(self.fig, master = self.base_root)
			self.ax = self.fig.add_subplot(111)
			self.ax.set_xlim(-0.1*self.x,1.1*self.x)
			self.ax.set_ylim(-0.1*self.y,1.1*self.y)
			self.ax.scatter(*zip(*self.coords), color=(0,0,1),picker=True)
			self.ax.set_aspect('equal')
			plt.grid()
			self.ax.set_title("Select a home base")
			self.cid = self.canvas.callbacks.connect('pick_event', self.onpick)
			self.canvas.draw()
			self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		else:
			self.windowMsg("You need to select points before selecting a base.")

	def aco_solve(self):
		self.field.updateSamples(self.coords,self.x,self.y,self.n_sample_carry)
		self.field.clusterize()
		if self.base:
			self.field.setCamp(self.base)
		path = self.field.compute_aco()
		path = path.tolist()
		self.path = path

		plot_root = Tk()
		fig = plt.figure()
		ax = fig.add_subplot(111)
		canvas = FigureCanvasTkAgg(fig, master = plot_root)

		for p in path:
			x,y,c = zip(*p)
			ax.set_xlim(-0.1*self.x,1.1*self.x)
			ax.set_ylim(-0.1*self.y,1.1*self.y)
			ax.plot(x,y, marker = 'o')
			ax.set_aspect('equal')
		print(path)

		canvas.draw()
		canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	def demo(self):
		plot_root = Tk()
		self.demo_fig = plt.figure()
		self.demo_ax = self.demo_fig.add_subplot(111)
		self.demo_canvas = FigureCanvasTkAgg(self.demo_fig, master = plot_root)
		controls = Tk()
		controls.geometry('200x200')
		next = Button(controls, text="Next", command=self.add_idx)
		next.pack(expand=True,fill='both')
		
		deploy = Button(controls, text="Deploy")
		deploy.pack(expand=True,fill='both')

		self.demo_pos = Label(controls, text = "To next node: ")
		self.demo_pos.pack(expand=True,fill='both')

		self.add_idx()

	def plot_partial(self, fig, ax, canvas, n=-1):
		points = []
		
		camp = self.field.returnCamp()
		camp_x = camp[0]
		camp_y = camp[1]
		for cluster in self.path:
			cluster_ordered = []
			for idx, pt in enumerate(cluster):
				if camp_x == pt[0] and camp_y == pt[1]:
					splt1 = cluster[idx:]
					splt2 = cluster[:idx]
					splt_idx = len(splt1)-1
					if splt_idx >= 0 and len(splt2) > 0:
						if splt1[splt_idx] == splt2[0]:
							splt2 = splt2[1:]
					cluster_ordered = splt1 + splt2
					break
			points = points + cluster_ordered

		print("CAMP IS " + str(camp))
		print(points)

		if n<0:
			n = len(points)

		points = points[:n]

		plt.cla()
		ax.set_xlim(-0.1*self.x,1.1*self.x)
		ax.set_ylim(-0.1*self.y,1.1*self.y)
		x,y,c = zip(*points)
		ax.set_title("Node " + str(self.node_idx))
		ax.plot(x,y, marker = 'o',color='tab:blue')
		ax.set_aspect('equal')

		canvas.draw()
		canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	def ani_update(self, i, line):
		line.set_data(self.ani_x[:i], self.ani_y[:i])
		if i == 60:
			self.anim.pause()
			#self.plot_partial(self.demo_fig,self.demo_ax,self.demo_canvas, n=self.node_idx)
		return line,

	def animate(self,pt1,pt2):
		print("ANIMATING")
		self.ani_x, self.ani_y = self.interpolate(pt1,pt2,60)
		#print(self.ani_x)
		#print(self.ani_y)
		line, = self.demo_ax.plot(self.ani_x[0],self.ani_y[0],color='tab:blue')
		self.anim = animation.FuncAnimation(self.demo_fig, self.ani_update, frames=len(self.ani_x)+5, fargs=[line], interval=25, blit=False, repeat=False)
		self.demo_canvas.draw()

	def interpolate(self, pt1, pt2, n):
		dx = pt2[0] - pt1[0]
		dy = pt2[1] - pt1[1]
		intp_x = []
		intp_y = []
		n = n-1
		for i in range(n):
			intp_x.append(pt1[0] + i*dx*(1/n))
			intp_y.append(pt1[1] + i*dy*(1/n))
		intp_x.append(pt2[0])
		intp_y.append(pt2[1])
		return (intp_x, intp_y)

	def getPt(self, n_idx):
		points = []
		
		camp = self.field.returnCamp()
		camp_x = camp[0]
		camp_y = camp[1]
		for cluster in self.path:
			cluster_ordered = []
			for idx, pt in enumerate(cluster):
				if camp_x == pt[0] and camp_y == pt[1]:
					splt1 = cluster[idx:]
					splt2 = cluster[:idx]
					splt_idx = len(splt1)-1
					if splt_idx >= 0 and len(splt2) > 0:
						if splt1[splt_idx] == splt2[0]:
							splt2 = splt2[1:]
					cluster_ordered = splt1 + splt2
					break
			points = points + cluster_ordered

		return points[n_idx-1]

	def add_idx(self):
		if self.node_idx > 0:
			self.plot_partial(self.demo_fig,self.demo_ax,self.demo_canvas, n=self.node_idx)
			self.node_idx = self.node_idx + 1
			print(self.node_idx)
			pt1 = self.getPt(self.node_idx-1)
			pt2 = self.getPt(self.node_idx)
			if pt1 == pt2:
				print("hi")
			#print(pt1)
			#print(pt2)
			self.update_demo_pos()
			self.animate(pt1[:2],pt2[:2])
		else:
			self.node_idx = self.node_idx + 1
			self.plot_partial(self.demo_fig,self.demo_ax,self.demo_canvas, n=self.node_idx)
			self.update_demo_pos()

	def update_demo_pos(self):
		pt1 = self.getPt(self.node_idx)
		pt2 = self.getPt(self.node_idx + 1)
		dy = pt2[1]-pt1[1]
		dx = pt2[0]-pt1[0]
		deg = math.tan(math.radians(dy/dx))
		dist = math.sqrt(dx**2 + dy**2)
		self.demo_pos.config(text = "To next node: " + str(round(dist,2)) + " m " + str(round(deg,2)) + " deg")

	def onclick(self, event):
		ix, iy = event.xdata, event.ydata
		print('x = %d, y = %d'%(ix, iy))

		if ix and iy:
			self.coords.append([ix, iy])

			self.ax.scatter(*zip(*self.coords), color=(0,0,1))
			self.canvas.draw()

		if len(self.coords) == self.n_nodes:
			print(self.coords)

			self.canvas.mpl_disconnect(self.cid)

			self.field = ACO(np.array(self.coords),self.x,self.y, sampleCapacity = self.n_sample_carry)
			#self.field.plot()
			plt.close(self.fig)
			self.empty_root.destroy()
			self.windowMsg("Nodes selected.")

	def onpick(self, event):
		self.canvas.mpl_disconnect(self.cid)
		self.base = self.coords[event.ind[0]]
		print(self.base)
		plt.close(self.fig)
		self.base_root.destroy()
		self.windowMsg("Base selected.")

def main():
	ui = NavUI()
	ui.root.mainloop()

if __name__ == "__main__":
	main()