#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from ruleparser import RuleParser
from predicateparser import PredicateParser
from api import *
from helper import *
import copy

class WumpusWorld:
	def __init__(self,predf,rulef):
		self.worlds = {	1 : [
								[0,0,0,0,-100,0,0,0],
								[0,0,0,0,0,0,-50,0],
								[0,0,0,0,0,0,0,-50],
								[0,-50,0,0,0,0,0,0],
								[0,0,0,-100,0,0,0,-100],
								[0,-50,0,-100,0,1000,0,0],
								[0,0,0,0,0,0,0,0],
								[0,0,-50,0,-50,0,0,0]					
							],
						2 : [
								[0,0,-50,0,0,-50,0,-100],
								[0,0,-50,0,-100,1000,0,0],
								[0,0,0,0,-50,0,0,0],
								[0,0,0,0,0,-100,0,0],
								[0,0,0,0,-50,0,0,0],
								[-100,0,0,0,-100,-50,0,0],
								[0,0,0,0,0,0,0,0],
								[-100,-100,0,0,0,0,0,0]					
							]}
						
		self.world = None
						
		self.fol = FOL()
		self.pp = PredicateParser()
		#self.pp.parse(predf)
		self.rp = RuleParser()
		rules = self.rp.parse(rulef)
		
		for r in rules:
			self.fol.tell(Rule(r))
						
			
	def getWorld(self):
		return copy.deepcopy(self.world)
		
	def setWorld(self,x):
		self.world = self.worlds[x]
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
			
	def dfs(self,stack,parentMap):
		visited = set()
		stack.append((0,0))
		while stack:
			x,y = stack.pop()
			p = 'P'+str(x)+str(y)
			self.fol.forget(Rule('Unvisited('+p+')'))
			self.fol.forget(Rule('~Visited('+p+')'))
			self.fol.tell(Rule('Visited('+p+')'))
			print p
			visited.add((x,y))
			if self.world[x][y] == -100:
				self.fol.tell(Rule('Wumpus('+p+')'))
			if self.world[x][y] == -50:
				self.fol.tell(Rule('Pit('+p+')'))
			if self.world[x][y] == 1000:
				self.fol.tell(Rule('Glitter('+p+')'))
			if self.IsGoal((x,y)):
				return (x,y)
			children = reversed(self.visit_children((x,y)))
			for child in children:
				if child not in visited:
					parentMap[child] = (x,y)
					stack.append(child)
		return None
		
	def IsGoal(self,pair):
		x,y = pair
		p = 'P'+str(x)+str(y)
		q = self.fol.ask(Query('EndGame('+p+')'))
		return q
		
	def visit_children(self,pair):
		x,y = pair
		dirx = [1,0,0,-1]
		diry = [0,1,-1,0]
		children = []
		for i in xrange(4):
			_x = x+dirx[i]
			_y = y+diry[i]
			if self.isValid(_x,_y):
				a = self.fol.ask(Query('Visited(P'+str(_x)+str(_y)+')'))
				if not a:
					b = self.fol.ask(Query('Dangerous(P'+str(_x)+str(_y)+')'))
					if not b:
						children.append((_x,_y))			
		return children
				
	def isValid(self,x,y):
		return (x >=0 and y >=0 and x<=7 and y<=7 and self.world[x][y]>=0)
		
	def Run(self):
		stack,parentMap = [],{}
		t = self.dfs(stack,parentMap)
		if isinstance(t,tuple):
			print "Gold found at : ",t,parentMap
			s = []
			while t in parentMap.keys():
				print t, parentMap[t]
				s.append(t)
				t = parentMap[t]
		else:
			print "Gold could not be found."
		return t,s

# ww =WumpusWorld('predicatefile2.txt','rulefile2.txt')
# ww.setWorld(1)
# ww.Run()