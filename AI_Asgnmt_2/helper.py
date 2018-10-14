#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from state import *
from random import *

def genBlocks(n):
	lst = []
	for i in range(n):
		lst.append(i+1)
	return lst
	
def genInitState(n,stlen):
	if n < stlen:
		return None
	lst = genBlocks(n)
	state = State([])
	for i in range(stlen):
		state.putStack(i)
	for i in range(len(lst)):
		j = randint(0,stlen-1)
		state.getStack(j).Push(Block(lst[i]))
	return state
	
def genGoalState(state,steps):
	cnt = steps
	prevsrc=-1
	prevdest=-1
	while cnt > 0:
		src = randint(0,state.getSize()-1)
		dest = randint(0,state.getSize()-1)
		if dest!=prevsrc and src!=prevdest:
			if src!=dest and state.getStack(src).getSize()> 0:
				newstate = state.transfer(src,dest)
				if newstate != None:
					state = newstate
					cnt-=1
					prevsrc = src
					prevdest = dest
	return state

def state_from_hash(hash):
	state = State([])
	for i,x in enumerate(hash):
		stack = Stack(i,[])
		for y in x:
			b = Block(y)
			stack.Push(b)
		state.pushStack(stack)
	return state
