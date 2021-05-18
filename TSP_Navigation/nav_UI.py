from tkinter import *
from ACO import *

import matplotlib.pyplot as plt

from bridson import poisson_disc_samples

class NavUI:
	def __init__(self):
		self.coords = []
		self.ax = None
		self.fig = None
		self.cid = None
		self.field = None
		self.pathcolletion = None

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
		coords = poisson_disc_samples(self.x, self.y, r=2)
		self.coords = coords
		locations = np.array(coords)
		np.random.shuffle(locations)
		self.field = ACO(locations, self.x, self.y, sampleCapacity = self.n_sample_carry)

		self.windowMsg("Generated nodes.")

	def emptyPlot(self):
			self.coords = []
			self.fig = plt.figure()
			self.ax = self.fig.add_subplot(111)
			plt.xlim(-0.1*self.x,1.1*self.x)
			plt.ylim(-0.1*self.y,1.1*self.y)
			plt.title("Select " + str(self.n_nodes) + " points")
			self.ax.set_aspect('equal')
			plt.grid()
			self.ax.plot()

			self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
			plt.show()

	def select_base(self):
		if self.field:
			self.fig = plt.figure()
			self.ax = self.fig.add_subplot(111)
			plt.xlim(-0.1*self.x,1.1*self.x)
			plt.ylim(-0.1*self.y,1.1*self.y)
			plt.scatter(*zip(*self.coords), color=(0,0,1),picker=True)
			self.ax.set_aspect('equal')
			plt.grid()
			plt.title("Select a home base")
			self.cid = self.fig.canvas.callbacks.connect('pick_event', self.onpick)
			plt.show()
		else:
			self.windowMsg("You need to select points before selecting a base.")

	def aco_solve(self):
		self.field.updateSamples(self.coords,self.x,self.y,self.n_sample_carry)
		self.field.clusterize()
		if self.base:
			self.field.setCamp(self.base)
		path = self.field.compute_aco()
		path = path.tolist()
		for p in path:
			x,y,c = zip(*p)
			plt.plot(x,y, marker = 'o')
		print(path)
		plt.show()

	def onclick(self, event):
		ix, iy = event.xdata, event.ydata
		print('x = %d, y = %d'%(ix, iy))

		if ix and iy:
			self.coords.append([ix, iy])

			self.ax.scatter(*zip(*self.coords), color=(0,0,1))
			plt.show()

		if len(self.coords) == self.n_nodes:
			print(self.coords)

			self.fig.canvas.mpl_disconnect(self.cid)

			self.field = ACO(np.array(self.coords),self.x,self.y, sampleCapacity = self.n_sample_carry)
			self.field.plot()
			plt.close(self.fig)

	def onpick(self, event):
		self.fig.canvas.mpl_disconnect(self.cid)
		self.base = self.coords[event.ind[0]]
		print(self.base)
		plt.close(self.fig)

def main():
	ui = NavUI()
	ui.root.mainloop()

if __name__ == "__main__":
	main()