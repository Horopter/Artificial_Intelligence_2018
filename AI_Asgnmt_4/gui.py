#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

import Tkinter as tk
import time
import copy
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
		
		self.root.attributes("-topmost", True)
		
	def doNothing(self):
		return
	
	def prepGrid(self,num=5):
		x1 = 13*self.width/30
		x2 = 9*self.width/10
		y1 = self.height/10
		y2 = 9*self.height/10
		self.canvas.create_line(x1,y1,x2,y1,fill="blue",width="5")
		self.canvas.create_line(x1,y1,x1,y2,fill="blue",width="5")
		self.canvas.create_line(x1,y2,x2,y2,fill="blue",width="5")
		self.canvas.create_line(x2,y2,x2,y1,fill="blue",width="5")
		for i in range(1,num):
			deltax = 14*self.width*i/(30*num)
			deltay = 8*self.height*i/(10*num)
			self.canvas.create_line(x1+deltax,y1,x1+deltax,y2,fill="red",width="5")
			self.canvas.create_line(x1,y1+deltay,x2,y1+deltay,fill="red",width="5")
			
	def putValues(self,num=5,d = {}):
		x1 = 13*self.width/30
		y1 = self.height/10
		dx = 14*self.width/(30*num)
		dy = 8*self.height/(10*num)
		x0,y0 = x1 + dx/2, y1 + dy/2
		
		for i in range(0,num):
			for j in range(0,num):
				x,y = x0 + j*dx, y0 + i*dy
				if i*num+j in d:
					self.canvas.create_text(x,y,text=str(d[i*num+j]),font=("Purisa", 20))

		
	def printResults(self,r):
		lst = r.values()
		for i in range(len(lst)):
			self.canvas.create_text(self.width/6,(i+1)*self.height/16,text=str("R"+str(i+1)+" : "+str(lst[i])))
	
	def update(self):
		self.root.update()
		
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
	g = GUI('Assignment 4')
	g.loop()