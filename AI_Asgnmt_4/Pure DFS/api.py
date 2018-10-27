
from state import *
from helper import *

def isGoal(node):
	state = node.state
	lst = state.arr
	return allEqual(lst)

def visit_children(node):
	index = node.index
	size = node.size
	state = node.state
	depth = node.depth
	children = []
	for e in state.domain:
		tempState = State(size,state.arr,state.domain)
		tempState.domain.remove(e)
		if index+1 < size*size:
			tempState.arr[index+1] = e
			children.append(Node(tempState,node,index+1,depth+1))
	return children
	
def dfs(initState,stack):
	visited = set()
	node = Node(initState,None,-1,0)
	stack.append(node)
	while len(stack) > 0:
		node = stack[-1]
		del stack[-1]
		if node.state.__hash__() not in visited:
			visited.add(node.state.__hash__())
			if node.depth == (node.size*node.size) and isGoal(node):
				return node
			children = reversed(visit_children(node))
			stack.extend(children)
			
if __name__ == '__main__':
	st = State(3)
	stk = []
	dfs(st,stk)
	