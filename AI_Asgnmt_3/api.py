#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from state import *
from helper import *
from random import *
import sys
import time

class GamePlan:
	def isValid(self,pos,size):
		return doesExist(pos,size)
		
	def boost(self,node):
		if node.coinCount <= 6:
			#There will be a lot many moves before forfeit. This will boost intelligence to counter delay effectively.
			self.depth = 5
	
	def gameStatus(self,state):
		node = Node(state, None, None, 0, 0, 1, None, None)
		self.boost(node)
		if node.coinCount<4 or (node.p1==0 or node.p2==0):
			if node.p1 > node.p2:
				return 1
			elif node.p1 < node.p2:
				return 2
			else:
				return 0
		return -1
		
	def getVal(self,board,pos):
		x,y = pos
		return board[x][y]
		
	def getPos(self,pos,dir,type):
		x,y = pos
		lst = [(-1,1),(0,2),(1,1),(1,-1),(0,-2),(-1,-1)]
		dx,dy = lst[dir]
		dest = x+dx*type,y+dy*type
		inter = None
		if type == 2:
			inter = x+dx,y+dy
		return inter,dest
		
	def opposite(self,player):
		if player>0:
			return 3-player
			
	def HASH(self,lst):
		if isinstance(lst,list):
			l = '['
			for x in lst:
				l = l+'|'+str(self.HASH(x))+'|'
			l = l + ']'
			return l
		return lst
		
	def Successors(self,node):
		coins = []
		size = node.state.size
		board = node.state.board
		player = node.player
		if player == 1:
			coins = node.p1Pos
		elif player == 2:
			coins = node.p2Pos
		children = []
		for i in range(0,len(coins)):#position
			for j in range(0,6):#direction
				for k in range(1,3):#type
					action = player,coins[i],j,k
					b = self.move(copy.deepcopy(board),action)
					if b != None:
						sb = State(b)
						if sb.__hash__() not in self.transposition:
							newNode = Node(sb, node, action, node.depth+1, node.cost+1, self.opposite(player), None, None)
							self.genNodes += 1
							self.nodeMem = max(sys.getsizeof(newNode),self.nodeMem)
							self.transposition[sb.__hash__()]=newNode
							children.append(newNode)
							
		if len(children)==0 and node.state.__hash__() not in self.transposition:
			newNode = Node(node.state, node, None, node.depth+1, node.cost+1, self.opposite(player), None, None) #Pass to other Player Scenario
			self.genNodes += 1
			self.nodeMem = max(sys.getsizeof(newNode),self.nodeMem)
			self.transposition[node.state.__hash__()]=newNode
			children.append(newNode)
			
		node.numChildren = len(children)
		shuffle(children)
		return children
		
	def EndGame(self,node):
		if node.depth==self.depth or node.numChildren == 0 or node.coinCount<4 or node.p1==0 or node.p2==0:
			return True
		return False
		
	def Utility(self,node):
		if node.utility is None:
			score1,score2,t1,t2 = Util(node.state.board)
			if self.MAXIMIZER == 1:
				return (2*score1 - 34*score2 + 5*t1 - 13*t2)
			elif self.MAXIMIZER == 2:
				return (2*score2 - 34*score1 + 5*t2 - 13*t1)
		
	def move(self,board,action):
		player,init,direction,type = action
		Board = copy.deepcopy(board)
		size = len(board),len(board[0])
		if self.isValid(init,size) and self.getVal(Board,init)== player:
			if type == 1:
				inter,dest = self.getPos(init,direction,type)
				if self.isValid(dest,size) and self.getVal(Board,dest)==0:
					x1,y1 = init
					x2,y2 = dest
					Board[x1][y1],Board[x2][y2] = Board[x2][y2],Board[x1][y1]
			elif type == 2:
				inter,dest = self.getPos(init,direction,type)
				if self.isValid(dest,size) and self.getVal(Board,dest)==0 and self.getVal(Board,inter)==self.opposite(player):
					x1,y1 = init
					x2,y2 = inter
					x3,y3 = dest
					Board[x1][y1],Board[x3][y3] = Board[x3][y3],Board[x1][y1]
					Board[x2][y2] = 0
					
		if self.HASH(board)==self.HASH(Board):
			return None
		return Board
	
	def __init__(self):
		self.recurse = 1
		self.genNodes = 0
		self.nodeMem = 0
		self.startTime = 0
		self.endTime = 0


class Minimax(GamePlan):
	def Decision(self,state,player):
	
		#Procedure Initialization
		self.transposition = {}
		node = Node(state, None, None, 0, 0, player, None, None)
		self.MAXIMIZER = node.player
		self.MINIMIZER = self.opposite(node.player)
		
		#Meta-data Initialization
		self.nodeMem = sys.getsizeof(node)
		self.genNodes += 1
		
		#Termination Check
		self.boost(node)
		
		#Time Keeping		
		self.startTime = time.time()
		n,v = self.MaxValue(node)
		# print "Best Sequence from now on : "
		# printAction(n,v)
		self.endTime = time.time()
		
		print "Max Util Value : ",v
		
		#Returning Values
		if n!=None:
			if n!=node:
				return n.action,(self.nodeMem,self.recurse,self.genNodes,self.endTime-self.startTime)
			else:
				return None,(self.nodeMem,self.recurse,self.genNodes,self.endTime-self.startTime) #Forfeit
		return None,(self.nodeMem,self.recurse,self.genNodes,self.endTime-self.startTime) #StaleMate
		
	def MaxValue(self,node):
		if self.EndGame(node):
			node.utility=self.Utility(node)
			return None,node.utility
		v = float('-inf')
		successors = self.Successors(node)
		s = None
		if len(successors) == 0:
			node.utility=self.Utility(node)
			return None,node.utility
		for succ in successors:
			if succ.utility is None:
				ms,mv = self.MinValue(succ)
				succ.utility = mv
				succ.child_nodes.append(ms)
			else:
				mv = succ.utility
			if mv > v:
				v = mv
				s = succ
		self.recurse = max(self.recurse,node.depth)
		return s,v
		
	def MinValue(self,node):
		if self.EndGame(node):
			node.utility=self.Utility(node)
			return None,node.utility
		v = float('+inf')
		successors = self.Successors(node)
		s = None
		if len(successors) == 0:
			node.utility=self.Utility(node)
			return None,node.utility
		for succ in successors:
			if succ.utility is None:
				ms,mv = self.MaxValue(succ)
				succ.utility = mv
				succ.child_nodes.append(ms)
			else:
				mv = succ.utility
			if mv < v:
				v = mv
				s=succ
		self.recurse = max(self.recurse,node.depth)
		return s,v

	def __init__(self,difficulty):
		if difficulty == 'E':
			self.depth = 3
		elif difficulty == 'M':
			self.depth = 5
		elif difficulty == 'H':
			self.depth = 7
		GamePlan.__init__(self)
		
class AlphaBeta(GamePlan):
	def Decision(self,state,player):
		#Procedure Initialization
		self.transposition = {}
		node = Node(state, None, None, 0, 0, player, None, None)
		self.MAXIMIZER = node.player
		self.MINIMIZER = self.opposite(node.player)
		
		#Meta-data Initialization
		self.nodeMem = sys.getsizeof(node)
		self.genNodes += 1
		
		#Termination Check
		self.boost(node)
		
		#Time Keeping		
		self.startTime = time.time()
		n,v = self.MaxValue(node,float('-inf'),float('+inf'))
		# print "Best Sequence from now on : "
		# printAction(n,v)
		self.endTime = time.time()
		
		# print "Max Util Value : ",v
		
		#Returning Values
		if n!=None:
			if n!=node:
				return n.action,(self.nodeMem,self.recurse,self.genNodes,self.endTime-self.startTime)
			else:
				return None,(self.nodeMem,self.recurse,self.genNodes,self.endTime-self.startTime) #Forfeit
		return None,(self.nodeMem,self.recurse,self.genNodes,self.endTime-self.startTime) #StaleMate
		
	def MaxValue(self,node,alpha,beta):
		if self.EndGame(node):
			node.utility=self.Utility(node)
			return None,node.utility
		v = float('-inf')
		successors = self.Successors(node)
		s = None
		if len(successors) == 0:
			node.utility=self.Utility(node)
			return None,node.utility
		for succ in successors:
			if succ.utility is None:
				ms,mv = self.MinValue(succ,alpha,beta)
				succ.utility = mv
				succ.child_nodes.append(ms)
			else:
				mv = succ.utility
			if mv > v:
				v = mv
				s = succ
			if v >= beta:
				return s,v
			alpha = max(alpha,v)
		self.recurse = max(self.recurse,node.depth)
		return s,v
		
	def MinValue(self,node,alpha,beta):
		if self.EndGame(node):
			node.utility=self.Utility(node)
			return None,node.utility
		v = float('+inf')
		successors = self.Successors(node)
		s = None
		if len(successors) == 0:
			node.utility=self.Utility(node)
			return None,node.utility
		for succ in successors:
			if succ.utility is None:
				ms,mv = self.MaxValue(succ,alpha,beta)
				succ.utility = mv
				succ.child_nodes.append(ms)
			else:
				mv = succ.utility
			if mv < v:
				v = mv
				s=succ
			if v<=alpha:
				return s,v
			beta = min(beta,v)
		self.recurse = max(self.recurse,node.depth)
		return s,v

	def __init__(self,difficulty):
		if difficulty == 'E':
			self.depth = 3
		elif difficulty == 'M':
			self.depth = 5
		elif difficulty == 'H':
			self.depth = 7
		GamePlan.__init__(self)
			
def ApiDriver(Algorithm,difficulty,start):
	size = (5,11)
	st = State(genInitBoard(size))	
	st.write()
	forfeit=[]
	status = 1
	visited = set()
	while True:
		print time.time()-start
		if str((st,status)) not in visited:
			visited.add(str((st,status)))
			mm = Algorithm(difficulty)
			action = mm.Decision(st,status)
			if action is None:
				forfeit.append(status)
			else:
				forfeit.append(0)
				st = State(mm.move(st.board,action))
				if action[3] == 2:
					print "Player : ",status," takes coin..."
			print (status,action)
			status = 3-status
			if len(forfeit)>4 and forfeit[-1]>0 and forfeit[-3]>0 and forfeit[-1]==forfeit[-3]:
				print "Player : ",forfeit[-1]," forfeits..."
				print
				print
				st.write()
				break
		else:
			print "It's a draw match fellas."
			print
			print
			st.write()
			break
	
if __name__ == '__main__':
	import time
	start = time.time()
	print start
	Algorithms = {'M':Minimax,'A':AlphaBeta}
	difficulty = 'H'
	Algorithm = Algorithms['A']
	ApiDriver(Algorithm,difficulty,start)
	end = time.time()
	print end
	print end - start
	
#ME (approx 3 seconds per step): 201 (3 minutes 21 seconds)
#MM (approx 13 seconds per step): 577 (9 minutes 37 seconds) 
#MH (approx 80 seconds per step) : 1717 (28 minutes 47 seconds) 
#AE (approx 10 seconds per step) : 114-165 (around 2 minutes)
#AM (approx 30 seconds per step) : 573 (9 minutes 33 seconds)
#AH (approx 120 seconds per step): 2134 (35 minutes 34 seconds)


		
		
	
	