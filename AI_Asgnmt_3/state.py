#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

import copy
from helper import *

class Coin:
	def __init__(self,col='black'):
		self.color = col
		
class State:
	def __init__(self,board=[[]]):
		self.size = (len(board),len(board[0]))
		if self.isListEmpty(board):
			self.board = genInitBoard(self.size)
		else:
			self.board = copy.deepcopy(board)

	def __hash__(self):
		lst = []
		try:
			for e in self.board:
				try:
					if e == None:
						lst.append('None')
					elif isinstance(e,list):
						lst.append(tuple(e))
				except:
					print "Except : ",e
		except:
			print self.board
		return tuple(lst)
		
	def write(self):
		writeBoard(self.board,self.size)
		
	def isCorner(self,x,y):
		return (count(self.board,x,y,self.size) == 3)
			
	def isListEmpty(self,inList):
		if isinstance(inList, list):
			for a in inList:
				if self.isListEmpty(a):
					return False
			return True
		return False
				
class Node:
	def __init__(self, state, parent, action, depth, cost, player, utility, numChildren):
		self.parent = None
		self.child_nodes=[]
		self.p1Pos = []
		self.p2Pos = []
		
		self.state = copy.deepcopy(state)
		self.parent = parent
		self.action = action
		self.depth = depth
		self.cost = cost
		self.player = player
		self.utility = utility
		self.numChildren = numChildren
		if self.state:
			self._hash_ = state.__hash__()
			
		if self.parent:
			self.parent.child_nodes.append(self)
			
		size = self.state.size
		for i in range(0,size[0]):
			for j in range(0,size[1]):
				if self.state.board[i][j]==1:
					self.p1Pos.append((i,j))
				elif self.state.board[i][j]==2:
					self.p2Pos.append((i,j))
		
		self.coinCount = len(self.p1Pos) + len(self.p2Pos)
		self.p1 = len(self.p1Pos)
		self.p2 = len(self.p2Pos)
		
		
	def show(self):
		a = 0
		if self.parent:
			a = self.parent._hash_
		print (self._hash_,self.action,self.depth,self.cost,self.player,a)

			
	
if __name__ == "__main__":
	A = State()
	
	
	