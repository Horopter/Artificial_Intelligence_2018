#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from helper import *
from state import Node
# from state import State2
from initialStateGen import initStateGen
from goalStateGen import countSquares,genGoals
import pickle
import copy
import timeit
import datetime
import os.path

def is_goal_state(current_state,goal_states):
	return current_state in goal_states

def createRootNode(start_state):
	return Node(start_state, -1, None, None, 0)

# def createRootNode2(start_state):
# 	return State2(start_state, -1, None, None, 0)

def dfs(start_state,max_stack_len, max_depth,visit_count,goal_states,stack,showProgress):
	visited = set()
	if showProgress:
		print "DFS may take time. Please wait between 5-15 minutes."
	stack.append(createRootNode(start_state))
	while stack:
		node = stack.pop()
		visited.add(node._hash_)
		if is_goal_state(node.state,goal_states):
			return node
		children = reversed(visit_children(node,visit_count))
		for child in children:
			if child._hash_ not in visited:
				stack.append(child)
				visited.add(child._hash_)
				if child.depth > max_depth[0]:
					max_depth[0] += 1
		if len(stack) > max_stack_len[0]:
			max_stack_len[0] = len(stack)
	return None

def bfs(start_state,max_stack_len, max_depth,visit_count,goal_states,queue,showProgress):
	visited = set()
	if showProgress:
		print "BFS is dependent on number of matchsticks present. Please wait between 5-20 minutes."
	queue.append(createRootNode(start_state))
	j=0
	while queue:
		L = len(queue)
		for i in range(0,L):
			node = queue[0]
			queue.remove(node)
			visited.add(node._hash_)
			if is_goal_state(node.state,goal_states):
				return node
			children = visit_children(node,visit_count)
			for child in children:
				if child._hash_ not in visited:
					queue.append(child)
					visited.add(child._hash_)
					if child.depth > max_depth[0]:
						max_depth[0] += 1
			if len(queue) > max_stack_len[0]:
				max_stack_len[0] = len(queue)
		if showProgress:
			print "Level completed ",j," ",L
		j+=1
	return None



def dls(start_state,max_stack_len, max_depth,visit_count,goal_states,stack,threshold):
	visited = set()
	stack.append(createRootNode(start_state))
	while stack:
		node = stack.pop()
		visited.add(node._hash_)
		if is_goal_state(node.state,goal_states):
			return node
		if node.depth < threshold:
			children = reversed(visit_children(node,visit_count))
			for child in children:
				if child._hash_ not in visited:
					stack.append(child)
					visited.add(child._hash_)
					if child.depth > max_depth[0]:
						max_depth[0] += 1
			if len(stack) > max_stack_len[0]:
				max_stack_len[0] = len(stack)
	return None

def ids(start_state,max_stack_len, max_depth,visit_count,goal_states,stack,showProgress):
	threshold = 1
	iterator = 0
	vs = 0
	print "IDS may take time according to depth and maximum branch factor. Please press Ctrl+C to exit the module at anytime."
	while iterator < len(start_state)+1:
		if showProgress:
			print "Checking with threshold:",threshold
		max_stack_len[0]=0
		max_depth[0]=0
		visit_count[0]=0
		#Empty the stack before beginning the procedure 
		while len(stack)>0:
			stack.pop()
		response = dls(start_state,max_stack_len, max_depth,visit_count,goal_states,stack,threshold)
		if response != None:
			visit_count[0] = vs
			return response
		else:
			threshold += 1
			if showProgress:
				print "Max Stack Length last iteration :",max_stack_len[0]
				print "Max Depth last iteration :",max_depth[0]
				print "Nodes visited last iteration :",visit_count[0]
		iterator+=1
		vs += visit_count[0]
	visit_count[0] = vs

def visit_children(node,visit_count):
	visit_count[0] += 1
	children = []
	for i in range(node.pos,len(node.state)):
		remove = act(node.state, i)
		if remove is not None:
			children.append(Node(remove, i+1, node, True, node.depth + 1))
	nodes = [child for child in children if child.pos <= len(child.state)]
	return nodes

def act(state, pos):
	new_state = copy.deepcopy(state)
	if pos+1 < len(new_state):
		if new_state[pos+1]:
			new_state[pos+1] = False #change
			return new_state
	return None

# def visit_children_2(node,visit_count):
# 	visit_count[0] += 1
# 	children = []
# 	i=node.pos
# 	remove = act_2(node.state, i, True)
# 	if remove is not None:
# 		children.append(State2(remove, i+1, node, True, node.depth + 1))
# 	skip = act_2(node.state, i, False)
# 	if skip is not None:
# 		children.append(State2(skip, i+1, node, False, node.depth + 1))
# 	nodes = [child for child in children if child.pos <= len(child.state)]
# 	return nodes

# def act_2(state, pos, action):
# 	new_state = copy.deepcopy(state)
# 	if pos+1 < len(new_state):
# 		if new_state[pos+1] and action:
# 			new_state[pos+1] = False #remove the stick
# 		return new_state
# 	return None

def getActions(actions,goal_node,initial_state):
	current_node = goal_node
	while current_node and initial_state != current_node.state:
		if current_node.action and initial_state[current_node.pos]:
			action = current_node.pos
			actions.insert(0, action)
		current_node = current_node.parent

def getInitSquares(size,pct,goal,showProgress=False):
	initial_state = initStateGen(size,pct)
	csq = countSquares(size,initial_state)
	if showProgress:
		print "Init :\n",initial_state
		print "Initial squares :",csq
	if (size*size*pct//100) < goal:
		return []
	if csq <= goal:
		if showProgress:
			print "Initial size: ",size
			print "Initial coverage:",pct
			print "Squares found:",csq
			print "Initial squares not sufficient for goal squares."
		return None
	return initial_state

def runAlgorithm(size,goal,algorithm,initial_state,showProgress=False):
	function_pointer = {
	'bfs': bfs,
	'dfs': dfs,
	'ids': ids
	}

	goals = []
	
	if os.path.exists(str(size)+"_"+str(goal)+".pkl") == False:
		print "Goal state list doesn't exist. Generating now..."
		genGoals(size,goal)
		print "Goal states generated."
	myfile = open(str(size)+"_"+str(goal)+".pkl","rb")
	goal_states = pickle.load(myfile)
	myfile.close()

	for x in goal_states:
		lst = genTuple(size)
		fillTuple(x,size,lst)
		goals.append(lst)

	max_aux_len = [0]
	max_depth=[0]
	visited_nodes=[0]
	auxiliary = []
	actions = []

	start = timeit.default_timer()
	if showProgress:
		print "Start Time: ",datetime.datetime.now()
	reached_goal = function_pointer[algorithm](initial_state,max_aux_len,max_depth,visited_nodes,goals,auxiliary,showProgress)
	if showProgress:
		print "Stop Time: ",datetime.datetime.now()
	stop = timeit.default_timer()
	if showProgress:
		print "Time taken is ",stop-start

	#analysis module
	if reached_goal is None:
		#This point should never be reached
		print "Your code is wrong."
		print "Initial state: ",initial_state
		print "Goal :",goal
		return []
	elif showProgress:
		print "Goal :",reached_goal.state
		print "Arm position at goal :",reached_goal.pos
		print "Depth of goal node :",reached_goal.depth
		print "Max Depth reached :",max_depth[0]
		print "Max Auxiliary Length :",max_aux_len[0]
		print "Number of nodes visited :",visited_nodes[0]

	getActions(actions,reached_goal,initial_state)
	
	if showProgress:
		print actions

	results=[initial_state,reached_goal,actions,max_depth[0],max_aux_len[0],visited_nodes[0],stop-start]
	return results

if __name__ == "__main__":
	size = 4
	pct = 50
	goal = 2
	start = timeit.default_timer()
	isq = getInitSquares(size,pct,goal,True)
	r = runAlgorithms(size,pct,goal,['dfs','ids','bfs'],isq,True)
	stop = timeit.default_timer()

