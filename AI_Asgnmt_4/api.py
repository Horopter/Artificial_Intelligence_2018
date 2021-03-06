#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************


import random
import copy
import time
import sys
import math
from helper import *

class Query(object):
	def __init__(self):
		self.Cons = []
		self.Vars = {}

	def setAlgorithm(self, algo):
		self.Algorithm = algo

	def declVar(self, var, dom):
		dom = Domain(dom)
		self.Vars[var] = dom

	def declVars(self, vars, dom):
		for var in vars:
			self.declVar(var, dom)

	def declCon(self, con, vars=None):
		self.Cons.append((con, vars))

	def getSol(self,valueOrder,forwardCheck, constraintProp,nodeSize,numNodes,curDepth,maxDepth):
		doms, cons, hcons = self.getParams()
		return self.Algorithm.getSol(doms, cons, hcons, valueOrder, forwardCheck, constraintProp, nodeSize,numNodes,curDepth,maxDepth)

	def getParams(self):
		#Set dom
		doms = copy.deepcopy(self.Vars)
		
		#Set cons
		cons = []
		for con, vars in self.Cons:
			cons.append((con, vars))
	
		#Set Hash of vars
		hcons = {}
		for var in doms:
			hcons[var] = []
		for con, vars in cons:
			for var in vars:
				hcons[var].append((con, vars))
					
		return doms, cons, hcons

class RBT():
	def backtrack(self, sols, doms, hcons,asgnmts, multiple, valueOrder, forwardCheck, constraintProp, nodeSize, numNodes, curDepth, maxDepth):
		
		numNodes[0] += 1
		nodeSize[0] = max(nodeSize[0],sys.getsizeof(sols)+sys.getsizeof(doms)+sys.getsizeof(hcons)+sys.getsizeof(asgnmts))
		maxDepth[0] = max(maxDepth[0],curDepth)
		seq = []
		
		if valueOrder == None:
			sqdct = {}
			for var in doms:
				sqdct[var] = (-len(hcons[var]),len(doms[var]), var)
			num = int(math.sqrt(len(doms)))
			sq = getSequence(num)
			seq = []
			for i in sq:
				seq.append(sqdct[i])
				
		else:
			seq = [(-len(hcons[var]),len(doms[var]), var) for var in doms]
			if valueOrder == True:
				seq.sort()
			
		for con, vars in hcons[var]:
			if not con(vars, doms, asgnmts,None):
				break

		for tuplet in seq:
			if tuplet[-1] not in asgnmts:
				break
		else:
			sols.append(asgnmts.copy())
			return sols

		var = tuplet[-1]
		asgnmts[var] = None
		
		if forwardCheck:
			hdoms = [doms[x] for x in doms if x not in asgnmts]
		else:
			hdoms = None

		for val in doms[var]:
			asgnmts[var] = val
			if hdoms:
				for dom in hdoms:
					dom.add()
			for con, vars in hcons[var]:
				if not con(vars, doms, asgnmts,hdoms):
					break
			else:
				# print "Assignment : ",asgnmts
				if constraintProp:
					y = self.ac3(doms,hcons,asgnmts)
					if y is not None:
						d,h,a = y
						self.backtrack(sols, d, h ,a, multiple, valueOrder, forwardCheck, constraintProp,nodeSize, numNodes, curDepth+1 , maxDepth)
					elif y is False:
						return sols
				else:
					self.backtrack(sols,doms,hcons,asgnmts, multiple, valueOrder, forwardCheck, constraintProp, nodeSize, numNodes, curDepth+1 , maxDepth)
				if sols and not multiple:
					return sols
			if hdoms:
				for dom in hdoms:
					dom.rem()
		del asgnmts[var]
		return sols

	def getSol(self, doms, cons, hcons, valueOrder, forwardCheck, constraintProp, nodeSize, numNodes, curDepth, maxDepth):
		sols = self.backtrack([], doms, hcons,{}, False, valueOrder, forwardCheck, constraintProp, nodeSize, numNodes, curDepth, maxDepth)
		return sols or None
		
	def rem_inconsistency(self, xi, xj, domains, asgnmts):
		removed = False
		for x in domains[xi]:
			if len(domains[xj]) == 1 and x in domains[xj]:
				l = list(domains[xi])
				l.remove(x)
				domains[xi] = Domain(l)
				asgnmts[xj] = domains[xj][0]
				domains[xj] = []
				removed = True
		return removed

	def eliminate(self,domains,asgnmts):
		for x in domains:
			for y in asgnmts:
				if asgnmts[y] in domains[x]:
					domains[x].remove(asgnmts[y])
					
	def ac3(self, domains, hcons, asgnmts):
		domains,hcons,asgnmts = copy.deepcopy(domains),copy.deepcopy(hcons),copy.deepcopy(asgnmts)
		self.eliminate(domains,hcons)	
		queue = []
		for xi in domains:
			for xj in hcons[xi]:
				if isinstance(xj[0],AllDiff): 
					for xk in xj[1]:
						if xi!=xk and (xi,xk) not in queue:
							queue.append((xk,xi))
				
				elif isinstance(xj[0],SumConstraint):
					s = 0
					for xk in xj[1]:
						if xk in asgnmts:
							s += asgnmts[xk]
							if s > xj[0].sum:
								return False
		while len(queue):
			xi, xj = queue.pop(0)
			if self.rem_inconsistency(xi, xj, domains, asgnmts):
				if not domains[xi]:
					return None
				for xj in hcons[xi]:
					if isinstance(xj[0],AllDiff): 
						for xk in xj[1]:
							if xi!=xk and (xk,xi) not in queue:
								queue.append((xk,xi))

		return domains,hcons,asgnmts
		

class Domain(list):
	def __init__(self, set):
		list.__init__(self, set)
		self.invisible = []
		self.visible = []

	def reset(self):
		self.extend(self.invisible)
		del self.invisible[:]
		del self.visible[:]

	def add(self):
		self.visible.append(len(self))

	def rem(self):
		diff = self.visible.pop() - len(self)
		if diff:
			self.extend(self.invisible[-diff:])
			del self.invisible[-diff:]

	def hide(self, val):
		list.remove(self, val)
		self.invisible.append(val)


class AllDiff():
	def __call__(self, vars, doms, asgnmts, fc=False):
		visited = {}
		for var in vars:
			val = asgnmts.get(var)
			if val is not None:
				if val in visited:
					return False
				visited[val] = True
		if fc:
			for var in vars:
				if var not in asgnmts:
					dom = doms[var]
					for val in visited:
						if val in dom:
							dom.hide(val)
							if not dom:
								return False
		return True


class SumConstraint():
	def __init__(self, sum):
		self.sum = sum

	def __call__(self, vars, doms, asgnmts, fc=False):
		sum = self.sum
		s = 0
		incomplete = False
		for var in vars:
			if var in asgnmts:
				s += asgnmts[var]
			else:
				incomplete = True
		if s > sum:
			return False
		if fc and incomplete:
			for var in vars:
				if var not in asgnmts:
					dom = doms[var]
					for val in dom[:]:
						if s + val > sum:
							dom.hide(val)
					if not dom:
						return False
		if incomplete:
			return s <= sum
		else:
			return s == sum		

def MagicSquare(num,valueOrder, forwardCheck, constraintProp):
	start = time.time()
	sq = num*num
	reqSum = num*(num*num+1)/2
	csp = Query()
	csp.setAlgorithm(RBT())
	csp.declVars(range(0, sq), range(1, sq + 1))
	csp.declCon(AllDiff(), range(0, sq))
	pd = [num*i+i for i in range(0,num)]
	sd = [num*i-i for i in range(1,num+1)]
	csp.declCon(SumConstraint(reqSum), pd)
	csp.declCon(SumConstraint(reqSum), sd)
	for row in range(num):
		csp.declCon(SumConstraint(reqSum),[row * num + i for i in range(num)])
	for col in range(num):
		csp.declCon(SumConstraint(reqSum),[col + num * i for i in range(num)])
	curDepth = 0
	nodeSize,numNodes,maxDepth = [0],[0],[0]
	sols = csp.getSol(valueOrder,forwardCheck,constraintProp,nodeSize,numNodes,curDepth,maxDepth)
	end = time.time()
	return (sols,nodeSize,numNodes,maxDepth,end-start)
	
if __name__ == '__main__':
	valueOrder, forwardCheck, constraintProp = True,True,False
	for i in range(1,6):
		MagicSquare(i,valueOrder, forwardCheck, constraintProp)