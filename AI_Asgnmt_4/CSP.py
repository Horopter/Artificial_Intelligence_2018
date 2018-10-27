import random
import copy
import time

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

	def getSol(self,valueOrder):
		doms, cons, hcons = self.getParams()
		return self.Algorithm.getSol(doms, cons, hcons, valueOrder)

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
	def __init__(self, fc=True):
		self.fc = fc

	def backtrack(self, sols, doms, hcons,asgnmts, multiple, valueOrder):
		seq = [(-len(hcons[var]),len(doms[var]), var) for var in doms]
		if valueOrder:
			seq.sort()
			
		#Select unassigned var
		for tuplet in seq:
			if tuplet[-1] not in asgnmts:
				break
		else:
			sols.append(asgnmts.copy())
			return sols

		var = tuplet[-1]
		asgnmts[var] = None

		fc = self.fc
		
		if fc:
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
				self.backtrack(sols, doms, hcons,asgnmts, multiple, valueOrder)
				if sols and not multiple:
					return sols
			if hdoms:
				for dom in hdoms:
					dom.remove()
		del asgnmts[var]
		return sols

	def getSol(self, doms, cons, hcons, valueOrder):
		sols = self.backtrack([], doms, hcons,{}, False, valueOrder)
		return sols or None

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

	def remove(self):
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

	def __call__(self, vars, doms, ass, fc=False):
		sum = self.sum
		s = 0
		incomplete = False
		for var in vars:
			if var in ass:
				s += ass[var]
			else:
				incomplete = True
		if s > sum:
			return False
		if fc and incomplete:
			for var in vars:
				if var not in ass:
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

def MagicSquare(num,valueOrder=True):
	print "Filling for ",num
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
	sols = csp.getSol(valueOrder)
	end = time.time()
	print "Time Taken : ",end-start
	
if __name__ == '__main__':
	for i in range(5,6):
		MagicSquare(i)