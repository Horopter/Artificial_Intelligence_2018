#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

import turtle
from math import *
X=1.0
Y=1.0
def drawGrid(color,indices,size,screen,quadrant,width):
	length = getSideLength(screen,size)
	center = getCenter(screen,quadrant)
	px,py = center
	stickpos=[]
	for i in indices:
		stickpos.append(getCoord(i,size))
	x,y = screen.screensize()
	px -= (size*length)*atan((y*1.0)/x)
	py += (size*length)*atan((y*1.0)/x)
	for pos in stickpos:
		tp = turtle.Turtle()
		tp.hideturtle()
		tp.penup()
		tp.color(color)
		tp.width(width)
		x,y,o = pos
		scalex = x*length
		scaley = -y*length
		scalex += px
		scaley += py
		tp.setpos(scalex,scaley)
		if o:
			tp.right(90)
		tp.pendown()
		tp.forward(length)
		tp.penup()

def getSideLength(screen,size):
	l = min(X,Y)
	l = l/5
	l = l/size
	return l

def getCenter(screen,quadrant):
	if quadrant == 1:
		return X/2,3*Y/4
	elif quadrant == 2:
		return 5*X/6,3*Y/4
	elif quadrant == 3:
		return X/2,Y/4 

def getCoord(i,size):
	modder = 2*size+1
	x = i%modder
	y = i/modder
	orientation = False #Horizontal
	if x >= size:
		x -= size
		orientation = True #Vertical
	return (x,y,orientation)

def getWindow():
	w = turtle.Screen()
	w.title('Assignment 1 - 2017H1030130P')
	w.setup(X,Y)
	w.setworldcoordinates(0,0,X,Y)
	return w

def runLoop():
	turtle.done()

def drawLine(a):
	x,y,orient,length = a
	tp = turtle.Turtle()
	tp.hideturtle()
	tp.penup()
	tp.setpos(x,y)
	tp.width(4)
	tp.color('green')
	if orient:
		tp.right(90)
	tp.pendown()
	tp.forward(length)
	tp.penup()

def partition(screen):
	x,y = screen.screensize()
	actions=[(X/3,Y,True,2*Y),(2*X/3,Y,True,2*Y),(X/3,Y/2,False,2*X/3)]
	for a in actions:
		drawLine(a)
	tp = turtle.Turtle()
	tp.hideturtle()
	x = X/2
	y = 96*Y/100
	tp.penup()
	tp.setpos(x,y)
	tp.write("G1", move=False, align="left", font=("Arial", 10, "normal"))
	x = 5*X/6
	y = 96*Y/100
	tp.penup()
	tp.setpos(x,y)
	tp.write("G2", move=False, align="left", font=("Arial", 10, "normal"))
	
def textit(algo,nodes_gen,mem_node,aux_len,actions,cost,time_req, pos):
	tp = turtle.Turtle()
	tp.hideturtle()
	x = 0
	y = 0
	if pos == 1:
		y = Y-0.04
	elif pos == 2:
		y = 2*Y/3-0.06
	pos-=1
	writeup = [" The algorithm used is "+str(algo).upper()+".",
				" (R"+str(pos*5+1)+") The number of nodes generated is "+str(nodes_gen)+".",
				" (R"+str(pos*5+2)+") The memory used per node is "+str(mem_node)+" bytes.",
				" (R"+str(pos*5+3)+") Maximum length of auxiliary stack/queue is "+str(aux_len)+".",
				" (G"+str(pos+1)+") The sticks to be removed are (zero-indexed): "+str(actions)+".",
				" (R"+str(pos*5+4)+") The cost is "+str(cost)+" units.",
				" (R"+str(pos*5+5)+") The time taken is "+str(time_req)+" seconds."]
	text = []
	for w in writeup:
		text.extend([w[i:i + 55] for i in xrange(0, len(w), 55)])
	for a,t in enumerate(text):
		tp.penup()
		tp.setpos(x,y-0.03*a)
		tp.write(t, move=False, align="left", font=("Arial", 10, "normal"))

def publish(analysis,cmp):
	tp = turtle.Turtle()
	tp.hideturtle()
	x = 0
	y = Y/5
	tp.penup()
	tp.setpos(x,y)
	txt = []
	if cmp == 1:
		txt = [" (R11) The algorithm "+analysis[1][0]+" uses more memory ("+str(analysis[1][1])+" bytes) than the algorithm "+analysis[0][0]+" ("+str(analysis[0][1])+" bytes) in the given scenario."]
	elif cmp == 0:
		txt = [" (R11) The algorithm "+analysis[1][0]+" uses same memory ("+str(analysis[1][1])+" bytes) than the algorithm "+analysis[0][0]+" ("+str(analysis[0][1])+" bytes) in the given scenario."]
	else:
		txt = [" (R11) The algorithm "+analysis[0][0]+" uses more memory ("+str(analysis[0][1])+" bytes) than the algorithm "+analysis[1][0]+" ("+str(analysis[1][1])+" bytes) in the given scenario."]
	text = []
	for w in txt:
		text.extend([w[i:i + 55] for i in xrange(0, len(w), 55)])
	for a,t in enumerate(text):
		tp.penup()
		tp.setpos(x,y-0.03*a)
		tp.write(t, move=False, align="left", font=("Arial", 10, "normal"))

def inform(a,b):
	tp = turtle.Turtle()
	tp.hideturtle()
	x = 0
	y = Y/9
	tp.penup()
	tp.setpos(x,y)
	txt = [" (R12) The average path computed by algorithm 1 is "+str(a)+" units and that by algorithm 2 is "+str(b)+" units."]
	text = []
	for w in txt:
		text.extend([w[i:i + 55] for i in xrange(0, len(w), 55)])
	for a,t in enumerate(text):
		tp.penup()
		tp.setpos(x,y-0.03*a)
		tp.write(t, move=False, align="left", font=("Arial", 10, "normal"))	