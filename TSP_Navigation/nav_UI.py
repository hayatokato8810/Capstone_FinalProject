from tkinter import *
from TSP_simulation import *

class NavUI:
	def __init__(self):
		self.root = Tk()  
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

		self.node_select = Button(self.root, text="Node Selection", command=self.select_nodes, width = 15)
		self.node_select.grid(column=0, row=6, columnspan = 2)

		self.aco_btn = Button(self.root, text="ACO Solve", command=self.aco_solve, width = 20)
		self.aco_btn.grid(column=3, row=0, columnspan = 2)

		self.aco_btn = Button(self.root, text="kCluster Solve", command=self.kcluster_solve, width = 20)
		self.aco_btn.grid(column=3, row=1, columnspan = 2)

		self.field = None
		self.nclusters = 0

	def update_settings(self):
		self.nclusters = 20//int(self.max_cluster_ent.get())
		print(self.max_cluster_ent.get())
		print(self.nclusters)
		print(self.field_x_ent.get())
		print(self.field_y_ent.get())
		return

	def select_nodes(self):
		emptyPlot()
		self.field = get_globalField()

	def aco_solve(self):
		path = self.field.aco(limit=100)
		self.field.plotNodes(acoPath=path)

	def kcluster_solve(self):
		self.field.kCluster(self.nclusters)
		self.field.plotNodes()

def main():
	ui = NavUI()
	ui.root.mainloop()

if __name__ == "__main__":
	main()