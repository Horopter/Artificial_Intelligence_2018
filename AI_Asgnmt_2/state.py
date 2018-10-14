#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

import copy

class Block:
	id = 0
	
	def __init__(self,id):
		self.id = id
		
	def getId(self):
		return self.id
		
	def __hash__(self):
		return (self.id)
		
	def show(self):
		print self.id
	
class Stack:
	id = 0
	arr = []
	size = 0
	
	def __init__(self,id,arr):
		self.id = id
		self.arr = copy.deepcopy(arr)
		self.size = len(arr)
		
	def Push(self,elem):
		if isinstance(elem,Block):
			self.arr.append(elem)
			self.size += 1
			return True
		return False
			
	def Pop(self):
		if self.isEmpty():
			return False
		else:
			self.size -= 1
			elem = self.arr[-1]
			del self.arr[-1]
			return elem
			
	def getTop(self):
		if self.size > 0:
			return self.arr[-1]
		return None
			
	def isEmpty(self):
		return len(self.arr) < 1
		
	def getId(self):
		return self.id
		
	def getSize(self):
		return self.size
		
	def getBlock(self,index):
		if index < self.size:
			return self.arr[index]
		return None
		
	def __hash__(self):
		return tuple(e.__hash__() for e in self.arr)
			
class State:
	arr = []
	size = 0
	def __init__(self,arr):
		self.arr = copy.deepcopy(arr)
		self.size = len(arr)
		
	def isTransferable(self,src):
		if self.arr[src].getSize() < 1:
			return False
		return True
		
	def transfer(self,src,dest):
		if self.isTransferable(src) and src < self.size and dest < self.size and src > -1 and dest > -1:
			newState = State(self.arr)
			elem = newState.arr[src].Pop()
			if elem != False:
				confirm = newState.arr[dest].Push(elem)
				if confirm:
					return newState
		return None
	
	def getStack(self,num):
		if num < self.size:
			return self.arr[num]
	
	def putStack(self,num):
		self.arr.append(Stack(num,[]))
		self.size +=1
	
	def pushStack(self,st):
		if isinstance(st,Stack):
			self.arr.append(st)
			self.size += 1
	
	def getSize(self):
		return self.size
	
	def __hash__(self):
		lst = []
		for e in self.arr:
			lst.append(e.__hash__())
		return tuple(lst)
		
	def show(self):
		t = self.__hash__()
		print str(t)
			
			
class Node:
	parent = None
	child_nodes=[]
	def __init__(self, state, parent, action, depth, cost, key, pos):
		self.state = copy.deepcopy(state)
		self.parent = parent
		self.action = action
		self.depth = depth
		self.cost = cost
		self.key = key
		self.stackpos = pos
		if self.state:
			self._hash_ = state.__hash__()
		self.addChildNode(parent,self)
		
	def show(self):
		a = 0
		if self.parent:
			a = self.parent._hash_
		print (self._hash_,self.action,self.depth,self.cost,self.key,self.stackpos,a)

	def addChildNode(self,parent,child):
		if parent is not None:
			parent.child_nodes.insert(0,child)
	
if __name__ == "__main__":
	A = Block(1)
	B = Block(2)
	C = Block(3)
	D = Block(4)
	E = Block(5)
	st1 = [A,B,C]
	st2 = [D,E]
	s1 = Stack(0,st1)
	s2 = Stack(1,st2)
	state = State([s1,s2])
	state.show()
	newState = state.transfer(0,1)
	newState.show()
	
	