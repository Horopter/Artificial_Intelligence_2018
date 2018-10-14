#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from state import *
from heapq import heappush, heappop, heapify
import itertools
import timeit

def visit_children(node,visit_count):
	visit_count[0] += 1
	children = []
	for i in range(0,node.state.getSize()):
		for j in range(0,node.state.getSize()):
			if i != j:
				children.append(act(node,i,j))
	nodes = [child for child in children if child is not None]
	return nodes

def act(node,src,dest):
	s = node.state.transfer(src,dest)
	if s is None:
		return None
	return  Node(s,node,(src,dest), node.depth+1, node.cost+1 , 0, src)
	
def equalRewardandPenalty(start_state,goal_state,showProgress):
	count = 0
	if showProgress:
		print "Evaluating cur state : ",start_state.show()
	for i in range(0,min(start_state.getSize(),goal_state.getSize())):
		si = start_state.getStack(i)
		gi = goal_state.getStack(i)
		for j in range(0,min(si.getSize(),gi.getSize())):
			sb = si.getBlock(j)
			gb = gi.getBlock(j)
			eval = 0
			if sb.getId() == gb.getId():
				eval = 1 
			else:
				eval = -1
			count += eval
			if showProgress:
				print sb.getId(),":",eval
	if showProgress:
		print "Evaluation : ",count
	return count

def greaterRewardThanPenalty(start_state,goal_state,showProgress):
	count = 0
	if showProgress:
		print "Evaluating cur state : ",start_state.show()
	for i in range(0,start_state.getSize()):#for each stack
		si = start_state.getStack(i)
		gi = goal_state.getStack(i)
		blocks = []
		for j in range(0,si.getSize()):#for each block
			sb = si.getBlock(j)
			gb = gi.getBlock(j)
			if sb is not None:
				eval = 0
				if gb is not None and sb.getId() == gb.getId() and (len(blocks) == 0 or blocks[-1] > 0):
					eval = 5
				else:
					eval = -2
				if showProgress:
					print sb.getId(),":",eval
				blocks.append(eval)
				count += (eval)
	if showProgress:
		print "Evaluation : ",count
	return count
	
def PositionalRewardStaticPenalty(start_state,goal_state,showProgress):
	count = 0
	if showProgress:
		print "Evaluating cur state : ",start_state.show()
	for i in range(0,start_state.getSize()):#for each stack
		si = start_state.getStack(i)
		gi = goal_state.getStack(i)
		blocks = []
		for j in range(0,si.getSize()):#for each block
			sb = si.getBlock(j)
			gb = gi.getBlock(j)
			if sb is not None:
				eval = 0
				if gb is not None and sb.getId() == gb.getId() and (len(blocks) == 0 or blocks[-1] > 0):
					eval = (j+1)*(j+1)
				else:
					eval = -1
				if showProgress:
					print sb.getId(),":",eval
				blocks.append(eval)
				count += (eval)
	if showProgress:
		print "Evaluation : ",count
	return count

def PositionalRewardPositionalPenalty(start_state,goal_state,showProgress):
	count = 0
	if showProgress:
		print "Evaluating cur state : ",start_state.show()
	for i in range(0,start_state.getSize()):#for each stack
		si = start_state.getStack(i)
		gi = goal_state.getStack(i)
		blocks = []
		for j in range(0,si.getSize()):#for each block
			sb = si.getBlock(j)
			gb = gi.getBlock(j)
			if sb is not None:
				eval = 0
				if gb is not None and sb.getId() == gb.getId() and (len(blocks) == 0 or blocks[-1] > 0):
					eval = (j+1)*(j+1)
				else:
					eval = -(j+1)
				if showProgress:
					print sb.getId(),":",eval
				blocks.append(eval)
				count += (eval)
	if showProgress:
		print "Evaluation : ",count
	return count
	
def PositionalExponentialReward(start_state,goal_state,showProgress):
	count = 0
	if showProgress:
		print "Evaluating cur state : ",start_state.show()
	for i in range(0,start_state.getSize()):#for each stack
		si = start_state.getStack(i)
		gi = goal_state.getStack(i)
		blocks = []
		for j in range(0,si.getSize()):#for each block
			sb = si.getBlock(j)
			gb = gi.getBlock(j)
			if sb is not None:
				eval = 0
				if gb is not None and sb.getId() == gb.getId() and (len(blocks) == 0 or blocks[-1] > 0):
					eval = (5**(i+1))*(2**(j+1))
				else:
					eval = -(3**(i+1))*(2**(j+1))
				if showProgress:
					print sb.getId(),":",eval
				blocks.append(eval)
				count += (eval)
	if showProgress:
		print "Evaluation : ",count
	return count

fpointer = {1:equalRewardandPenalty,2:greaterRewardThanPenalty,3:PositionalRewardStaticPenalty,4:PositionalRewardPositionalPenalty,5: PositionalExponentialReward}
	
def hillClimbing(start_state,max_aux_len,max_depth,visit_count,goal_state,aux,heuristic,desiredGoal,graph,showProgress):
	root = Node(start_state, None, None, 0, 0, 0, -100000)
	visited = set()
	itr = 1
	while True:
		visited.add(root._hash_)
		r = fpointer[heuristic](root.state,goal_state,showProgress)
		print "Step Counter : ",itr
		graph.append((itr,r))
		children = visit_children(root,visit_count)
		nextEval = -100000
		nextNode = None
		for child in children:
			if child._hash_ not in visited:
				t = fpointer[heuristic](child.state,goal_state,showProgress)
				if t > nextEval:
					nextNode = child
					nextEval = t
					if showProgress:
						print "Next Eval : ",nextEval
						nextNode.show()
		if nextEval < r:
			if root._hash_ == goal_state.__hash__():
				print "Required goal reached!"
				desiredGoal[0]=True
			return root
		if showProgress:
			print "Root before: "
			root.show()
		root = nextNode
		if showProgress:
			print "Root after: "
			root.show()
		if child.depth > max_depth[0]:
			max_depth[0] += 1
		itr+=1
	
def astar(start_state,max_heap_len,max_depth,visit_count,goal_state,heap,heuristic,desiredGoal,graph,showProgress):
	visited, heap, heapmap, counter = set(), list(), {}, itertools.count()
	key = fpointer[heuristic](start_state,goal_state,showProgress)
	gg = fpointer[heuristic](goal_state,goal_state,showProgress)
	ig = fpointer[heuristic](start_state,goal_state,showProgress)
	print "InitState Eval : ",ig
	print "GoalState Eval : ",gg
	root = Node(start_state, None, None, 0, 0, key, -100000)
	entry = (-key, None, root)
	heappush(heap, entry)
	heapmap[root._hash_] = entry
	cnt = 1
	while heap:
		node = heappop(heap)
		cg = fpointer[heuristic](node[2].state,goal_state,showProgress)
		print "Step Counter : ",cnt,", current state eval : ",cg," goal state eval : ",gg
		graph.append((cnt,cg))
		visited.add(node[2]._hash_)
		if cg==gg:
			print "Goal Reached!",cg
			if goal_state.__hash__() == node[2].state.__hash__():
				print "Required goal reached!"
				desiredGoal=[2]
			return node[2]
		children = visit_children(node[2],visit_count)
		for child in children:
			child.key = child.cost + fpointer[heuristic](child.state,goal_state,showProgress)
			entry = (-child.key, child.action, child)
			if child._hash_ not in visited or child.stackpos == -100000:
				heappush(heap, entry)
				visited.add(child._hash_)
				heapmap[child._hash_] = entry
				if child.depth > max_depth[0]:
					max_depth[0] += 1
			elif (child._hash_ in heapmap or child.stackpos == -100000) and child.key < heapmap[child._hash_][2].key:
				try:
					hidx = heap.index((heapmap[child._hash_][2].key,
										 heapmap[child._hash_][2].move,
										 heapmap[child._hash_][2]))
					heap[int(hidx)] = entry
					heapmap[child._hash_] = entry
					heapify(heap)
				except:
					print "Already processed"
		if len(heap) > max_heap_len[0]:
			max_heap_len[0] = len(heap)
		cnt += 1
		
def bestFirstSearch(start_state,max_heap_len,max_depth,visit_count,goal_state,heap,heuristic,desiredGoal,graph,showProgress):
	visited, heap, heapmap, counter = set(), list(), {}, itertools.count()
	key = fpointer[heuristic](start_state,goal_state,showProgress)
	gg = fpointer[heuristic](goal_state,goal_state,showProgress)
	ig = fpointer[heuristic](start_state,goal_state,showProgress)
	print "InitState Eval : ",ig
	print "GoalState Eval : ",gg
	root = Node(start_state, None, None, 0, 0, key, -100000)
	entry = (-key, None, root)
	heappush(heap, entry)
	heapmap[root._hash_] = entry
	cnt = 0
	node = None
	while heap:
		node = heappop(heap)
		cg = fpointer[heuristic](node[2].state,goal_state,showProgress)
		print "Step Counter : ",cnt,", current state eval : ",cg," goal state eval : ",gg
		visited.add(node[2]._hash_)
		if cg==gg:
			print "Goal Reached!",cg
			if goal_state.__hash__() == node[2].state.__hash__():
				print "Required goal reached!"
				desiredGoal=[2]
			return node[2]
		children = visit_children(node[2],visit_count)
		for child in children:
			child.key = fpointer[heuristic](child.state,goal_state,showProgress)
			entry = (-child.key, child.action, child)
			if child._hash_ not in visited or child.stackpos == -100000:
				heappush(heap, entry)
				visited.add(child._hash_)
				heapmap[child._hash_] = entry
				if child.depth > max_depth[0]:
					max_depth[0] += 1
			elif (child._hash_ in heapmap or child.stackpos == -100000) and child.key < heapmap[child._hash_][2].key:
				try:
					hidx = heap.index((heapmap[child._hash_][2].key,heapmap[child._hash_][2].move,heapmap[child._hash_][2]))
					heap[int(hidx)] = entry
					heapmap[child._hash_] = entry
					heapify(heap)
				except:
					print "Already processed"
		if len(heap) > max_heap_len[0]:
			max_heap_len[0] = len(heap)
		cnt += 1
		

		
algos = {1:hillClimbing,2:astar,3:bestFirstSearch}

def getActions(actions,goal_node,initial_state):
	current_node = goal_node
	while current_node and initial_state and initial_state.__hash__() != current_node.state.__hash__():
		if current_node.action:
			action = current_node.action
			actions.insert(0, action)
		current_node = current_node.parent
			
def runAlgorithm(initial_state,goal_state,algo,heuristic,showProgress=False):
	max_aux_len = [0]
	max_depth=[0]
	visited_nodes=[0]
	auxiliary = []
	actions = []
	desiredGoal = [False]
	algorithm = algos[algo]
	graph = []
	start = timeit.default_timer()
	reached_goal = algorithm(initial_state,max_aux_len,max_depth,visited_nodes,goal_state,auxiliary,heuristic,desiredGoal,graph,showProgress)
	end = timeit.default_timer()
	getActions(actions,reached_goal,initial_state)
	print "start time : ",start
	print "end time : ",end
	return (algorithm.__name__,max_aux_len,max_depth,visited_nodes,auxiliary,actions,desiredGoal,reached_goal,end-start,graph)

			
if __name__ == "__main__":
	from helper import *
	ll = []
	for i in range(1,3):
		l = []
		for j in range(1,11):
			init = genInitState(200,j*10)
			goal = genGoalState(init,10)
			l.append((j*10,runAlgorithm(init,goal,i,2)[-2]))
		ll.append(l)
	print ll
	
	