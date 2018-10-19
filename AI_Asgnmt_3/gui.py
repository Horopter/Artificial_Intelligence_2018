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

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc

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
		
		self.circles = {}
		self.lines = {}
		self.locationBindings = {}
		self.doubleClickBindings = {}
		self.spaceBindings = {}
		self.selected = None
		self.bsize = (5,11)
		self.Action = None
		self.activation = -1
		self.player = 0
		
		self.aux = []
		self.nextButton = None
		
	def doNothing(self):
		return
	
	def setPlayer(self,id):
		self.player = id
	
	def activate(self,actid):
		self.activation = actid
		if self.activation == -1:
			self.canvas.bind('<1>',self.doNothing())
		else:
			self.canvas.unbind('<1>')
		
	def getAction(self):
		return self.Action
		
	def setCurState(self,state):
		self.curState = state
		self.bsize = self.curState.size
		
	def getCurState(self):
		return copy.deepcopy(self.curState)
		
	def setup(self):
		widthSpace = 10
		heightSpace = 0.1*(self.height)
		ox = self.width/3 + 50
		oy = self.height*0.7
		xspace = ((2*self.width/3)-widthSpace)/self.bsize[1]
		yspace = self.height/10
		lw = 3
		
		circles = {}
		locationBindings = {}
		spaceBindings = {}
		lines = []
		
		for i in range(0,self.bsize[0]):
			for j in range(0,self.bsize[1]):
				if j<self.bsize[1]-2 and self.curState.board[i][j]!=-1 and self.curState.board[i][j+2]!=-1 and (ox+j*xspace,oy-i*yspace,ox+(j+2)*xspace,oy-(i)*yspace) not in lines:
					self.line(ox+j*xspace,oy-i*yspace,ox+(j+2)*xspace,oy-(i)*yspace,fill="blue",width=lw)
					lines.append((ox+j*xspace,oy-i*yspace,ox+(j+2)*xspace,oy-(i)*yspace))
					
				if j<self.bsize[1]-2 and i<3 and self.curState.board[i][j]!=-1 and self.curState.board[i+2][j+2]!=-1 and (ox+j*xspace,oy-i*yspace,ox+(j+2)*xspace,oy-(i+2)*yspace) not in lines:
					self.line(ox+j*xspace,oy-i*yspace,ox+(j+2)*xspace,oy-(i+2)*yspace,fill="blue",width=lw)
					lines.append((ox+j*xspace,oy-i*yspace,ox+(j+2)*xspace,oy-(i+2)*yspace))
				
				if j>1 and i<3 and self.curState.board[i][j]!=-1 and self.curState.board[i+2][j-2]!=-1 and (ox+j*xspace,oy-i*yspace,ox+(j-2)*xspace,oy-(i+2)*yspace) not in lines:
					self.line(ox+j*xspace,oy-i*yspace,ox+(j-2)*xspace,oy-(i+2)*yspace,fill="blue",width=lw)
					lines.append((ox+j*xspace,oy-i*yspace,ox+(j-2)*xspace,oy-(i+2)*yspace))
					
				c = None
				bnd = None
				value = self.curState.board[i][j]
				if value!=-1:
					c = self.circle(ox+j*xspace,oy-i*yspace,self.getColor(0))
					circles[c] = (i,j,0,None)
					locationBindings[(i,j,0)] = c
					spaceBindings[(i,j)] = (ox+j*xspace,oy-i*yspace)
				if value==1:
					c = self.circle(ox+j*xspace,oy-i*yspace,self.getColor(value),'g('+str(i)+','+str(j)+')')
					bnd = self.canvas.tag_bind(c, "<Button-1>", self.select)
					self.canvas.tag_raise(c)
				elif value==2:
					c = self.circle(ox+j*xspace,oy-i*yspace,self.getColor(value),'r('+str(i)+','+str(j)+')')
					bnd = self.canvas.tag_bind(c, "<Button-1>", self.select)
					self.canvas.tag_raise(c)
				if c!=None:
					circles[c] = (i,j,value,bnd)
					locationBindings[(i,j,value)] = c
					spaceBindings[(i,j)] = (ox+j*xspace,oy-i*yspace)
					
		self.circles = circles
		self.locationBindings = locationBindings
		self.spaceBindings = spaceBindings
		self.lines = lines
		self.update()
		
	def select(self,event):
		if self.activation == -1 and self.player != 2:
			return
		if self.selected!=None:
			self.canvas.itemconfig(self.selected,outline="#7EC0EE")
		id = event.widget.find_closest(event.x, event.y)[0]
		self.selected = id
		if self.selected in self.circles and self.circles[self.selected][2] != 1:
			self.selected = None
			return
		self.canvas.itemconfig(self.selected,outline='blue') 
		moves = self.getMoves(self.circles[self.selected][0],self.circles[self.selected][1])
		self.resetDoubleClickBinding()
		doubleClickBindings = {}
		for x in moves:
			obj = self.locationBindings[(x[0],x[1],0)]
			self.canvas.itemconfig(obj,fill='purple') 
			doubleClickBindings[obj]=self.canvas.tag_bind(obj, "<Double-Button-1>", self.drop)
		self.doubleClickBindings = doubleClickBindings
		self.update()
			
	def resetDoubleClickBinding(self):
		if len(self.doubleClickBindings)>0:
			for x in self.doubleClickBindings:
				self.canvas.tag_unbind("<Double-Button-1>",self.doubleClickBindings[x])
				self.canvas.itemconfig(x,fill=self.getColor(self.circles[x][2]))
		self.doubleClickBindings = {}
		self.update()
			
	def prepMove(self,flag=False):
		inter,dest = self.getPos(self.Action[1],self.Action[2],self.Action[3])
		x1,y1 = self.Action[1]
		x2,y2 = dest
		p1 = self.Action[0]
		if flag:
			if self.selected is None:
				self.selected = self.locationBindings[(x1,y1,p1)]
				
			self.canvas.itemconfig(self.selected,outline='blue') 
			moves = self.getMoves(self.circles[self.selected][0],self.circles[self.selected][1])
			self.resetDoubleClickBinding()
			for x in moves:
				obj = self.locationBindings[(x[0],x[1],0)]
				self.canvas.itemconfig(obj,fill='purple')
			self.update()
			self.pause(1)
			for x in moves:
				obj = self.locationBindings[(x[0],x[1],0)]
				self.canvas.itemconfig(obj,fill=self.getColor(self.circles[obj][2]))
			
	def getPos(self,pos,dir,type):
		x,y = pos
		lst = [(-1,1),(0,2),(1,1),(1,-1),(0,-2),(-1,-1)]
		dx,dy = lst[dir]
		dest = x+dx*type,y+dy*type
		inter = None
		if type == 2:
			inter = x+dx,y+dy
		return inter,dest	
		
	def move(self,action=None):
		if self.activation == -1 and self.player != 2:
			return
		if action is not None:
			self.Action = action
			self.prepMove(True)
		if self.selected is None:
			return
		if self.Action is not None:
			inter,dest = self.getPos(self.Action[1],self.Action[2],self.Action[3])
			x1,y1 = self.Action[1]
			x2,y2 = dest
			p1 = self.Action[0]
			
			srcx,srcy = self.spaceBindings[(x1,y1)]
			destx,desty = self.spaceBindings[(x2,y2)]
			
			if (x2-x1)**2 + (y2-y1)**2 == 2:#diagonal empty neighbors
				self.animateMove(self.selected,srcx,srcy,destx,desty)
				val = self.circles[self.selected][2]
				bnd = self.circles[self.selected][3]
				self.circles[self.selected] = (x2,y2,val,bnd)
				self.locationBindings[(x2,y2,p1)] = self.selected
				del self.locationBindings[(x1,y1,p1)]
				self.curState.board[x1][y1],self.curState.board[x2][y2] = self.curState.board[x2][y2],self.curState.board[x1][y1]
			
			elif x2-x1 == 0 and abs(y2-y1) == 4:#axial jump neighbors
				self.animateMove(self.selected,srcx,srcy,destx,desty)
				val = self.circles[self.selected][2]
				bnd = self.circles[self.selected][3]
				self.circles[self.selected] = (x2,y2,val,bnd)
				self.locationBindings[(x2,y2,p1)] = self.selected
				del self.locationBindings[(x1,y1,p1)]
				self.curState.board[x1][y1],self.curState.board[x2][y2] = self.curState.board[x2][y2],self.curState.board[x1][y1]
				removed = self.locationBindings[(x1+(x2-x1)/2,y1+(y2-y1)/2,self.opposite(p1))]
				self.curState.board[x1+(x2-x1)/2][y1+(y2-y1)/2] = 0
				del self.circles[removed]
				del self.locationBindings[(x1+(x2-x1)/2,y1+(y2-y1)/2,self.opposite(p1))]
				self.canvas.delete(removed)
			
			elif x2-x1 == 0:#axial empty neighbors
				self.animateMove(self.selected,srcx,srcy,destx,desty)
				val = self.circles[self.selected][2]
				bnd = self.circles[self.selected][3]
				self.circles[self.selected] = (x2,y2,val,bnd)
				self.locationBindings[(x2,y2,p1)] = self.selected
				del self.locationBindings[(x1,y1,p1)]
				self.curState.board[x1][y1],self.curState.board[x2][y2] = self.curState.board[x2][y2],self.curState.board[x1][y1]
				
			else:#diagonal jump neighbors
				self.animateMove(self.selected,srcx,srcy,destx,desty)
				val = self.circles[self.selected][2]
				bnd = self.circles[self.selected][3]
				self.circles[self.selected] = (x2,y2,val,bnd)
				self.locationBindings[(x2,y2,p1)] = self.selected
				del self.locationBindings[(x1,y1,p1)]
				self.curState.board[x1][y1],self.curState.board[x2][y2] = self.curState.board[x2][y2],self.curState.board[x1][y1]
				removed = self.locationBindings[(x1+(x2-x1)/2,y1+(y2-y1)/2,self.opposite(p1))]
				self.curState.board[x1+(x2-x1)/2][y1+(y2-y1)/2] = 0
				del self.circles[removed]
				del self.locationBindings[(x1+(x2-x1)/2,y1+(y2-y1)/2,self.opposite(p1))]
				self.canvas.delete(removed)
				
				
			self.update()
			self.canvas.itemconfig(self.selected,outline="#7EC0EE")
			self.selected = None
			self.resetDoubleClickBinding()
			self.update()
			
	def gcd(self,x,y):
		while(y): 
			x, y = y, x % y 
		return abs(x)
			
	def getDir(self,dx,dy):
		lst = [(-1,1),(0,1),(1,1),(1,-1),(0,-1),(-1,-1)]
		return lst.index((dx,dy))
		
	def getType(self,x,g):
		if x==0 and g==2:
			return 1
		elif x == 0 and g==4:
			return 2
		elif g == 2:
			return 2
		else:
			return 1
			
	def drop(self,event):
		if self.activation == -1 and self.player != 2:
			return
		widthSpace = 10
		ox = self.width/3 + 50
		oy = self.height*0.7
		xspace = ((2*self.width/3)-widthSpace)/self.bsize[1]
		yspace = self.height/10
		id = event.widget.find_closest(event.x, event.y)[0]
		for x in self.doubleClickBindings:
			if x != id:
				self.canvas.tag_unbind("<Double-Button-1>",self.doubleClickBindings[x])
				self.canvas.itemconfig(x,fill=self.getColor(self.circles[x][2])) 
				
		x1,y1,p1,bind1 = self.circles[self.selected]
		x2,y2,p2,bind2 = self.circles[id]
		g = self.gcd(x2-x1,y2-y1)
		self.Action = (p1,(x1,y1),self.getDir((x2-x1)/g,(y2-y1)/g),self.getType(x2-x1,g))
		self.move()
		self.update()
				
	def animateMove(self,obj,x1,y1,x2,y2):
		incx = (x2-x1)/10
		incy = (y2-y1)/10
		for i in range(9):
			self.canvas.move(obj,incx,incy)
			self.update()
			if self.selected!=None:
				self.canvas.tag_raise(self.selected)
			self.pause(0.1)
			self.update()
			
		self.canvas.move(obj,x2-9*incx-x1,y2-9*incy-y1)
		self.update()
		if self.selected!=None:
			self.canvas.tag_raise(self.selected)
		self.pause(0.1)
		self.update()
			
	def opposite(self,num):
		return 3-num
	
	def getMoves(self,x,y):
		board = self.curState.board
		moves = []
		for i in range(-1,2):
			for j in range(-1,2):
				#diagonal empty neighbors
				if x+i>-1 and x+i<self.bsize[0] and y+j>-1 and y+j<self.bsize[1] and (i*i+j*j == 2):
					if board[x+i][y+j]==0:
						moves.append(((x+i),(y+j)))
				#axial empty neighbors
				if y+2*j>-1 and y+2*j<self.bsize[1] and i==0:
					if board[x][y+2*j]==0:
						moves.append((x,(y+2*j)))
				#diagonal jump neighbors		
				if x+2*i>-1 and x+2*i<self.bsize[0] and y+2*j>-1 and y+2*j<self.bsize[1] and (i*i+j*j != 0):
					if board[x+i][y+j]==self.opposite(board[x][y]) and  board[x+2*i][y+2*j]==0:
						moves.append(((x+2*i),(y+2*j)))
				#axial empty neighbors
				if y+4*j>-1 and y+4*j<self.bsize[1] and i==0:
					if board[x][y+4*j]==0 and board[x][y+2*j]==self.opposite(board[x][y]):
						moves.append((x,(y+4*j)))
		return moves
	
	def circle(self,x,y,clr,tag=None):
		if tag!=None:
			return self.canvas.create_circle(x, y, 20, fill=clr, outline="#7EC0EE", width=4,tag=tag)
		return self.canvas.create_circle(x, y, 20, fill=clr, outline="#7EC0EE", width=4)
		
	def line(self,x1,y1,x2,y2,fill,width):
		return self.canvas.create_line(x1,y1,x2,y2,fill=fill,width=width)
		
	def update(self):
		self.root.update()
	
	def color(self,object,clr):
		self.canvas.itemconfig(object,fill=clr)
		
	def getColor(self,num):
		if num == 0:
			return 'yellow'
		elif num == 1:
			return 'red'
		elif num==2:
			return 'green'
		
	def printResults(self,r):
		numNodes1 = "Number of nodes generated for the Minimax game : "+str(r[0])
		MemoryOfNode =  "Memory per node is "+str(r[1])+" bytes."
		MaxRecurse = "Maximum Depth of Recursion : "+str(r[2])
		timeElapsed1 = "Time Elapsed for the Minimax game \n(including delays by user) : "+str(r[3])+" seconds."
		nodesPerMicroSecond = "Number of nodes generated \n per microsecond : "+str(r[4])
		numNodes2 = "Number of nodes generated for the AlphaBeta game : "+str(r[5])
		ratio = "Saving using pruning (as a ratio) : "+str(r[6])
		timeElapsed2 = "Time Elapsed for the AlphaBeta game \n(including delays by user) : "+str(r[7])+" seconds."
		memoryVerdict = "On an Average, for depth more than 3,\n AlphaBeta uses less memory than Minimax."
		timeVerdict = "Average time for 10 games is 15 minutes on easy mode for AlphaBeta \n and 20 minutes for Minimax including user delays."
		AIWinsVerdict1 = "On an average, of 10 games, AI won 5 games, \n it was a draw 2 times with AlphaBeta of medium mode."
		AIWinsVerdict2 = "On an average, of 20 games, AI won 7 games, \n it was a draw 3 times with AlphaBeta of medium mode."
		FinalVerdict = "Minimax takes a lot of time as depth of search increases, than AlphaBeta."
		lst = [numNodes1,MemoryOfNode,MaxRecurse,timeElapsed1,nodesPerMicroSecond,numNodes2,ratio,timeElapsed2]
		for i in range(len(lst)):
			self.canvas.create_text(self.width/6,(i+1)*self.height/16,text=str("R"+str(i+1)+" : "+lst[i]))
		
		
	def delete(self,objects):
		for i in self.blocks:
			self.canvas.delete(self.blocks[i][1])
			self.canvas.delete(self.blocks[i][2])
			self.update()
		for i in self.aux:
			self.canvas.delete(i)
		self.actions = None
		self.curState = None
		self.itr=0

	def loop(self):
		self.root.mainloop()
		
	def exit(self):
		try:
			self.root.destroy()
		except:
			print "Application Destroyed."
		
	def pause(self,t=1):
		time.sleep(t)
		
if __name__ == '__main__':
	g = GUI('Assignment 3')
	init = State(genInitBoard((5,11)))
	g.setCurState(init)
	g.setup()
	g.loop()