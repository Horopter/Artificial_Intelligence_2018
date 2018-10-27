import copy

from helper import *

class State:
	def __init__(self,size,arr=None,domain=None):
		self.size = size
		
		if arr is None:
			self.arr = []
			for i in range(size*size):
				self.arr.append(0)
		else:
			self.arr = copy.deepcopy(arr)
			
		if domain is None:
			self.domain = set()
			for i in range(size*size):
				self.domain.add(i+1)
		else:
			self.domain = copy.deepcopy(domain)
			
	def pop(self,index):
		if index > -1 and index < size*size:
			if self.arr[index] != 0:
				self.domain.add(self.arr[index])
		self.arr[index] = 0
		
	def push(self,ind,elem):
		self.pop(ind)
		self.arr[ind] = elem
		
	def __hash__(self):
		return tuple(self.arr)
		
class Node:
	def __init__(self,state,parent,index,depth):
		self.child_nodes = []
		self.parent = parent
		self.state = copy.deepcopy(state)
		self.index = index
		self.size = self.state.size
		self.depth = depth
		
	def addChild(self,node):
		self.child_nodes.append(node)
		
	def __hash__(self):
		return self.state.__hash__()
	
	def printMe(self):
		print "\n"
		size = self.size
		for i in range(size):
			for j in range(size):
				print self.state.arr[i*size+j]," ",
			print 
		print "\n"