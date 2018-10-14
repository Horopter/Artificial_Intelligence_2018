#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

import Tkinter as tk
import time
import copy
from state import *
from helper import *
from random import *

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=1
        self._geom='200x200+0+0'
        self.master.geometry("{0}x{1}+0+0".format(
            self.master.winfo_screenwidth()-pad, self.master.winfo_screenheight()-pad))
        self.master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom=geom

class GUI:
	
	def __init__(self,title=""):
		self.root=tk.Tk()
		self.root.title(title)
		self.app=FullScreenApp(self.root)
		self.root.configure(bg="white")
		self.width = self.root.winfo_screenwidth()
		self.height = self.root.winfo_screenheight()
		self.canvas = tk.Canvas(self.root,width=self.width,height=self.height,bg="white")
		self.canvas.pack()
		self.canvas.create_line(self.width/3,0,self.width/3,self.height,fill="green",width="5")
		self.canvas.create_text(self.width/6,0.06*self.height,text="Algorithm 1 : HillClimbing\n Algorithm 2 : A*")
		self.blocks = {}
		self.aux = []
		self.nextButton = None
		self.reset()
		
	def setInitState(self,state):
		self.reset()
		self.initState = state
		
	def reset(self):
		if self.blocks:
			self.delete(self.blocks)
		self.blocks = {}
		if self.aux:
			self.delete(self.aux)
		self.aux = []
		if self.canvas and self.nextButton:
			self.nextButton.destroy()
			self.canvas.delete(self.nextButton)
		self.nextButton=None
		self.goalState = None
		self.actions = None
		self.itr=0
		self.update()

	def drawGraph(self,arr,loc,color):
		ydist = 0.43*self.height/10
		xdist = 0.26*self.width/10
		arrg = []
		if loc == 1:
			origin = [0.38*self.width,0.45*self.height]
		elif loc == 2:
			origin = [0.71*self.width,0.45*self.height]
		elif loc == 3:
			origin = [0.38*self.width,0.95*self.height]
		for i in arr:
			x,y,_x,_y = i
			arrg.append((origin[0]+x*xdist,origin[1]-y*ydist,_x,_y))
		self.lineGraph(arrg,color)
			
	def drawPartition(self):
		self.canvas.create_line(self.width/3,self.height/2,self.width,self.height/2,fill="green",width="5")
		self.canvas.create_line(2*self.width/3,0,2*self.width/3,self.height,fill="green",width="5")
		
	def graphSetup(self):
		self.canvas.create_line(0.38*self.width,0.45*self.height,0.64*self.width,0.45*self.height,fill="red",width="3")
		self.canvas.create_line(0.38*self.width,0.45*self.height,0.38*self.width,0.02*self.height,fill="red",width="3")
		self.canvas.create_text(self.width/2,0.47*self.height,text="Iterations")
		self.canvas.create_text(0.34*self.width,0.25*self.height,text="Heuristics",anchor="nw")
		self.canvas.create_line(0.71*self.width,0.45*self.height,0.97*self.width,0.45*self.height,fill="red",width="3")
		self.canvas.create_line(0.71*self.width,0.45*self.height,0.71*self.width,0.02*self.height,fill="red",width="3")
		self.canvas.create_text(7*self.width/8,0.47*self.height,text="Iterations")
		self.canvas.create_text(0.67*self.width,0.25*self.height,text="Heuristics",anchor="nw")
		self.canvas.create_line(0.38*self.width,0.95*self.height,0.64*self.width,0.95*self.height,fill="red",width="3")
		self.canvas.create_line(0.38*self.width,0.95*self.height,0.38*self.width,0.52*self.height,fill="red",width="3")
		self.canvas.create_text(self.width/2,0.90*self.height,text="Size")
		self.canvas.create_text(0.34*self.width,0.75*self.height,text="Time",anchor="nw")
		
	def lineGraph(self,arr,color):
		for i in range(len(arr)-1):
			x1,y1,x1l,y1l = arr[i]
			x2,y2,x2l,y2l = arr[i+1]
			self.canvas.create_line(x1,y1,x2,y2,fill=color,width="2")
			d = randint(0,3)
			ss = ""
			for i in range(d):
				if d%2 == 0:
					ss = ss+" "
				else:
					ss = ss+"\n"
			self.canvas.create_text(x1,y1,text=ss+"("+str(x1l)+","+str(y1l)+")"+ss)
			
		
	def setGoalState(self,state):
		self.goalState = state
		
	def nextStep(self):
		self.nextButton.config(state="disabled")
		if self.actions and self.itr < len(self.actions): 
			print "Move : ",self.itr+1," of ",len(self.actions)
			
			action = self.actions[self.itr]
			src,dest = action
			
			_idsrc = self.initState.getStack(src).getTop().getId()
			idsrc,srcBlock,srcLbl=self.blocks[_idsrc]
			self.color(srcBlock,"red")
			self.update()
			self.pause()

			self.move([srcBlock,srcLbl],dest,self.initState.getStack(dest).getSize(),self.initState.getSize())
			self.color(srcBlock,"green")
			self.update()
			self.pause()
			self.initState = self.initState.transfer(src,dest)

			self.color(srcBlock,"orange")
			self.update()
			self.itr+=1
		if self.itr >= len(self.actions):
			self.nextButton.config(state="disabled")
		else:
			self.nextButton.config(state="normal")
		
	def createNext(self,actions):
		self.actions = copy.deepcopy(actions)
		self.itr = 0
		if self.canvas and self.nextButton:
			self.canvas.delete(self.nextButton)
		self.nextButton = tk.Button(self.canvas,command=lambda:self.nextStep(), text="Next",height=2,width=10)
		self.nextButton.place(x=0.9*self.width,y=0.02*self.height)
	
	def setupStack(self,stacklen):
		p = 4
		s = (2*self.width/3-p*(stacklen+1))/stacklen
		aux = []
		for i in range(stacklen):
			r = self.canvas.create_rectangle(p+(s+p)*i+self.width/3,0.85*self.height,(s+p)*(i+1)+self.width/3,0.9*self.height,fill="purple")
			self.root.update()
			aux.append(r)
		return aux
		
	def representState(self):
		blocks ={}
		stacklen = self.initState.getSize()
		aux = self.setupStack(stacklen)
		p = 10
		s = (2*self.width/3-p*(stacklen+1))/stacklen
		ht = 2*self.height/(10*stacklen)
		for i in range(stacklen):
			st = self.initState.getStack(i)
			sz = st.getSize()
			for j in range(sz):
				b = st.getBlock(j)
				id = b.getId()
				tlw,tlh,brw,brh=p+(s+p)*i+self.width/3,0.85*self.height-ht*(j+1),(s+p)*(i+1)+self.width/3-p,0.85*self.height-ht*(j)-2
				rect = self.canvas.create_rectangle(tlw,tlh,brw,brh,fill="orange")
				label = self.canvas.create_text(((tlw+brw)/2,(tlh+brh)/2), text=str(id))
				blocks[id]=(id,rect,label)
		self.update()
		self.blocks = blocks
		self.aux = aux
		
	def create_label(self,arg,string):
		if arg == 'r1':
			self.r1 = self.canvas.create_text(self.width/6,0.12*self.height,text=string)
		elif arg == 'r2':
			self.r2 = self.canvas.create_text(self.width/6,0.18*self.height,text=string)
		elif arg == 'r3':
			self.r3 = self.canvas.create_text(self.width/6,0.24*self.height,text=string)
		elif arg == 'r5':
			self.r5 = self.canvas.create_text(self.width/6,0.30*self.height,text=string)
		elif arg == 'r6':
			self.r6 = self.canvas.create_text(self.width/6,0.36*self.height,text=string)
		elif arg == 'r7':
			self.r7 = self.canvas.create_text(self.width/6,0.42*self.height,text=string)
		elif arg == 'r8':
			self.r8 = self.canvas.create_text(self.width/6,0.48*self.height,text=string)
		elif arg == 'r10':
			self.r10 = self.canvas.create_text(self.width/6,0.54*self.height,text=string)
		elif arg == 'r11':
			self.r11 = self.canvas.create_text(self.width/6,0.60*self.height,text=string)
		elif arg == 'r12':
			self.r12 = self.canvas.create_text(self.width/6,0.66*self.height,text=string)
		
		
	
	def update(self):
		self.root.update()
	
	def color(self,object,clr):
		self.canvas.itemconfig(object,fill=clr)
		
	def move(self,objects,i,j,stacklen):
		p = 10
		s = (2*self.width/3-p*(stacklen+1))/stacklen
		ht = 2*self.height/(10*stacklen)
		tlw,tlh,brw,brh=p+(s+p)*i+self.width/3,0.85*self.height-ht*(j+1),(s+p)*(i+1)+self.width/3-p,0.85*self.height-ht*(j)-2
		self.canvas.coords(objects[0],tlw,tlh,brw,brh)
		self.canvas.coords(objects[1],(tlw+brw)/2.0,(tlh+brh)/2.0)
		
	def delete(self,objects):
		for i in self.blocks:
			self.canvas.delete(self.blocks[i][1])
			self.canvas.delete(self.blocks[i][2])
			self.update()
		for i in self.aux:
			self.canvas.delete(i)
		self.actions = None
		self.initState = None
		self.itr

	def loop(self):
		self.root.mainloop()
		
	def pause(self):
		time.sleep(1)