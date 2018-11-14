from api import *
from helper import Rule,Query

class WumpusWorld:
	def __init__(self):
		self.world = 	[
							[0,0,0,0,-100,0,0,0],
							[0,0,0,0,0,0,-50,0],
							[0,0,0,0,0,0,0,-50],
							[0,-50,0,0,0,0,0,0],
							[0,0,0,-100,0,0,0,-100],
							[0,-50,0,-100,0,1000,0,0],
							[0,0,0,0,0,0,0,0],
							[0,0,-50,0,-50,0,0,0]					
						]
						
		self.fol = FOL()
		self.fol.tell(Rule('Neighbors(x,y) -> Neighbors(y,x)'))
		self.fol.tell(Rule('Stench(x) & Neighbor(y,x) & (~ Visited(y)) & Visited(x) -> Dangerous(y)'))
		self.fol.tell(Rule('Breeze(x) & Neighbor(y,x) & (~ Visited(y)) & Visited(x) -> Dangerous(y)'))
		self.fol.tell(Rule('Wumpus(x) -> EndGame(x)'))
		self.fol.tell(Rule('Pit(x) -> EndGame(x)'))
		self.fol.tell(Rule('Gold(x) -> EndGame(x)'))
		self.fol.tell(Rule('Glitter(x) -> Gold(x)'))
		self.fol.tell(Rule('Safe(x) -> (~Dangerous(x))'))
		self.fol.tell(Rule('Dangerous(x) -> (~Safe(x))'))
		self.fol.tell(Rule('Unvisited(x) -> (~Visited(x))'))
		self.fol.tell(Rule('Visited(x) -> (~Unvisited(x))'))
		
		dirx = [-1,0,1,0]
		diry = [0,1,0,-1]
		for i in xrange(8):
			for j in xrange(8):
				_p = 'P'+str(i)+str(j)
				self.fol.tell(Rule('Unvisited('+_p+')'))
				for k in xrange(4):
					_x = i+dirx[k]
					_y = j+diry[k]
					if self.isValid(_x,_y):
						p = 'P'+str(_x)+str(_y)
						self.fol.tell(Rule('Neighbor('+p+','+_p+')'))
						if self.world[i][j]==-100:
							self.fol.tell(Rule('Stench('+p+')'))
						if self.world[i][j]==-50:
							self.fol.tell(Rule('Breeze('+p+')'))				
	
	def setPos(self,x,y):
		self.x = x
		self.y = y
		
	def setDir(self,dir):
		self.dir = dir
		
	def turn(self,deg):
		self.dir = self.DIRECTION[(self.dir+(deg/90))%4]
		
	def dfs(self,stack):
		visited = set()
		stack.append((0,0))
		self.fol.tell(Rule('Safe(P00)'))
		while stack:
			x,y = stack.pop()
			p = 'P'+str(x)+str(y)
			self.fol.forget(Rule('Unvisited('+p+')'))
			self.fol.forget(Rule('~Visited('+p+')'))
			self.fol.tell(Rule('Visited('+p+')'))
			print 'Visited('+p+')'
			visited.add((x,y))
			if self.world[x][y] == -100:
				self.fol.tell(Rule('Wumpus('+p+')'))
			if self.world[x][y] == -50:
				self.fol.tell(Rule('Pit('+p+')'))
			if self.world[x][y] == 1000:
				self.fol.tell(Rule('Glitter('+p+')'))
			if self.is_goal_state((x,y)):
				return (x,y)
			children = reversed(self.visit_children((x,y)))
			for child in children:
				if child not in visited:
					stack.append(child)
		return None
		
	def is_goal_state(self,pair):
		x,y = pair
		p = 'P'+str(x)+str(y)
		q = self.fol.ask(Query('EndGame('+p+')'))
		print "Goal State check : ",p,q
		return q
		
	def visit_children(self,pair):
		x,y = pair
		dirx = [1,0,0,-1]
		diry = [0,1,-1,0]
		children = []
		for i in xrange(4):
			_x = x+dirx[i]
			_y = y+diry[i]
			print x,y,_x,_y
			if self.isValid(_x,_y):
				a = self.fol.ask(Query('Visited(P'+str(_x)+str(_y)+')'))
				print "Visited : ",'P'+str(_x)+str(_y)+' : ',a
				if not a:
					b = self.fol.ask(Query('Dangerous(P'+str(_x)+str(_y)+')'))
					print "Dangerous : ",'P'+str(_x)+str(_y)+' : ',b
					if not b:
						children.append((_x,_y))
		print children				
		return children
				
	def isValid(self,x,y):
		return (x >=0 and y >=0 and x<=7 and y<=7 and self.world[x][y]>=0)
		
	def Run(self):
		stack = []
		print self.dfs(stack)
		
ww = WumpusWorld()
ww.Run()