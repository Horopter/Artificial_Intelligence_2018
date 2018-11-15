#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

import Tkinter as tk
from marcus import *
from wumpus import *

class GUI:
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("1000x600")

		self.problem = tk.IntVar()
		self.query = tk.IntVar()
		self.worldmap = tk.IntVar()
		
		self.slaves = []
		self.labels = []
		
		R1 = tk.Radiobutton(self.root, text="Option 1", variable=self.problem, value=1, command=self.paneChange)
		R1.place(x=80,y=200,anchor='w')
		R1.config(font=("Courier", 12))
		R2 = tk.Radiobutton(self.root, text="Option 2", variable=self.problem, value=2, command=self.paneChange)
		R2.place(x=80,y=250,anchor='w')
		R2.config(font=("Courier", 12))

		self.label = tk.Label(self.root)
		self.label.pack()

		self.m,self.ww = None,None
		self.root.mainloop()

	def paneChange(self):
		self.clear()
		self.sel()

	def clear(self):
		if len(self.slaves)>0:
			while len(self.slaves) > 0:
				self.slaves[0].place_forget()
				self.slaves[0].destroy()
				del self.slaves[0]
				self.root.update()
		while len(self.labels)>0:
			del self.labels[0]
				
	def ask(self):
		if self.m != None:
			a = self.m.Query(self.query.get()-1)
			self.labels[self.query.get()-1].config(text = str(a)) 
			
	def draw(self,mat):
		if self.canvas:
			self.canvas.destroy()
			self.canvas = tk.Canvas(self.root,width=800,height=500,background='white')
			self.canvas.place(x=250,y=40,anchor='nw')
			for i in range(9):
				self.canvas.create_line(50,30+i*50,635,30+i*50, fill="blue")
				self.canvas.create_line(50+i*73,30,50+i*73,430, fill="blue")
				
			for i in range(8):
				for j in range(8):
					if mat[i][j] == -100:
						self.canvas.create_oval(50+j*73+5,30+i*50+5,50+j*73+68,30+i*50+45,fill='red')
					if mat[i][j] == -50:
						self.canvas.create_oval(50+j*73+5,30+i*50+5,50+j*73+68,30+i*50+45,fill='brown')
					if mat[i][j] == 1000:
						self.canvas.create_oval(50+j*73+5,30+i*50+5,50+j*73+68,30+i*50+45,fill='gold')			
		
	def search(self):
		selection = "You selected the option " + str(self.problem.get())+ "\n You've chosen world #"+ str(self.worldmap.get()) + " Please wait for 20 minutes until DFS search completes."
		self.label.config(text = selection)
		
		self.ww.setWorld(self.worldmap.get())
		self.matrix = self.ww.getWorld()
		self.draw(self.matrix)
		# for rb in self.slaves:
			# rb.configure(state=tk.DISABLED)
		self.root.update()
		t,p = self.ww.Run()
		# for rb in self.slaves:
			# rb.configure(state=tk.ENABLED)
		for i,a in enumerate(p):
			if i!=0:
				x,y = a
				self.canvas.create_oval(50+y*73+5,30+x*50+5,50+y*73+68,30+x*50+45,fill='green')
				self.canvas.create_text(50+y*73+10,30+x*50+10,text=str(len(p)-i))
			
	def sel(self):
		selection = "You selected the option " + str(self.problem.get())
		self.label.config(text = selection)
		
		if self.problem.get() == 1:
			self.m = Marcus()
			self.m.DefineProblem('predicatefile1.txt','rulefile1.txt')
			
			q1 = tk.Radiobutton(self.root, text="Alive(Marcus,x) & Now(x)", variable=self.query, value=1, command=self.ask)
			q1.place(x=300,y=60,anchor='nw')
			q2 = tk.Radiobutton(self.root, text="TryAssassinate(x,Caesar)", variable=self.query, value=2, command=self.ask)
			q2.place(x=300,y=120,anchor='nw')
			q3 = tk.Radiobutton(self.root, text="Loyal(Marcus,Caesar)", variable=self.query, value=3, command=self.ask)
			q3.place(x=300,y=180,anchor='nw')
			q4 = tk.Radiobutton(self.root, text="Ruler(x)", variable=self.query, value=4, command=self.ask)
			q4.place(x=300,y=240,anchor='nw')
			q5 = tk.Radiobutton(self.root, text="Erupted(Volcano,x)", variable=self.query, value=5, command=self.ask)
			q5.place(x=300,y=300,anchor='nw')
			q6 = tk.Radiobutton(self.root, text="Dead(Marcus,60)", variable=self.query, value=6, command=self.ask)
			q6.place(x=300,y=360,anchor='nw')
			q7 = tk.Radiobutton(self.root, text="Hate(Marcus,Caesar)", variable=self.query, value=7, command=self.ask)
			q7.place(x=300,y=420,anchor='nw')
			q8 = tk.Radiobutton(self.root, text="Alive(Marcus,35)", variable=self.query, value=8, command=self.ask)
			q8.place(x=300,y=480,anchor='nw')
			
			a1 = tk.Label(self.root)
			a1.place(x=800,y=60,anchor='n')
			a2 = tk.Label(self.root)
			a2.place(x=800,y=120,anchor='n')
			a3 = tk.Label(self.root)
			a3.place(x=800,y=180,anchor='n')
			a4 = tk.Label(self.root)
			a4.place(x=800,y=240,anchor='n')
			a5 = tk.Label(self.root)
			a5.place(x=800,y=300,anchor='n')
			a6 = tk.Label(self.root)
			a6.place(x=800,y=360,anchor='n')
			a7 = tk.Label(self.root)
			a7.place(x=800,y=420,anchor='n')
			a8 = tk.Label(self.root)
			a8.place(x=800,y=480,anchor='n')
			
			self.slaves.extend([q1,q2,q3,q4,q5,q6,q7,q8,a1,a2,a3,a4,a5,a6,a7,a8])
			self.labels.extend([a1,a2,a3,a4,a5,a6,a7,a8])
			for a in self.slaves:
				a.config(font=("Courier", 12))
		
		elif self.problem.get() == 2:
			self.ww = WumpusWorld('predicatefile2.txt','rulefile2.txt')
			
			self.canvas = tk.Canvas(self.root,width=800,height=500,background='white')
			self.canvas.place(x=250,y=40,anchor='nw')
			choice1 = tk.Radiobutton(self.root, text="First Scenario", variable=self.worldmap, value=1, command=self.search)
			choice1.place(x=500,y=550,anchor='nw')
			choice2 = tk.Radiobutton(self.root, text="Second Scenario", variable=self.worldmap, value=2, command=self.search)
			choice2.place(x=750,y=550,anchor='nw')
			
			self.slaves.extend([self.canvas,choice1,choice2])