#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from helper import *
from unification import *
from itertools import product
import random
import abc

F,x,y,t= map(Stmt, 'Fxyt')

def CheckDefiniteClause(t):
	if t == None:
		return False
	elif isinstance(t,bool):
		return True
	elif IsTerm(t.operator):
		return True
	elif t.operator == '->':
		ante, cons = t.operands
		return (IsTerm(cons.operator) and all(IsTerm(term.operator) for term in Expand('&',[ante]) if isinstance(term,Stmt)))
	else:
		return False

def Parse(t):
	assert CheckDefiniteClause(t)
	if isinstance(t,bool) or IsTerm(t.operator):
		return [], t
	else:
		ante, cons = t.operands
		return Expand('&',[ante]), cons

def Constants(x):
	if isinstance(x,int):
		return {x}
	elif not isinstance(x, Stmt):
		return set()
	elif IsTerm(x.operator) and x.operator[0].isupper() and not x.operands:
		return {x}
	else:
		return {sym for term in x.operands for sym in Constants(term)}


def Expand(operator, operands):
	result = []
	def Append(statement):
		for term in statement:
			if isinstance(term,Stmt) and term.operator == operator:
				Append(term.operands)
			else:
				result.append(term)
	Append(operands)
	return result


class FOL():
	def __init__(self, init=None):
		self.clauses = []
		self.tell(True)
		self.tell(False)
		if init:
			for clause in init:
				self.tell(clause)

	def tell(self, sentence):
		if CheckDefiniteClause(sentence):
			self.clauses.append(sentence)
		else:
			raise ValueError("Invalid Clause")
			
	def forget(self, sentence):
		if sentence in self.clauses:
			self.clauses.remove(sentence)

	def ask(self, query):
		x = self.querygen(query)
		return First(x, default=False)
		
	def querygen(self, query):
		return forward_chain(self, query)

	def display(self):
		for x in self.clauses:
			try:
				print Parse(x)
			except:
				print "Done."

def forward_chain(fol, A):
	constFOL = list({x for clause in fol.clauses for x in Constants(clause)})
	constFOL.extend(list({x for x in Constants(A)}))
	#print "CFOL : ",constFOL
	def substitute(p):
		qv = list({x for clause in p for x in Vars(clause)})
		for subList in product(constFOL, repeat=len(qv)):
			T = {a: b for a, b in zip(qv, subList)}
			yield T
	for q in fol.clauses:
		Phi = Unify(q, A, {})
		if Phi == {}:
			yield True
		if Phi != None:
			yield Phi
	while True:
		new = []
		for rule in fol.clauses:
			ante, cons = Parse(rule)
			for T in substitute(ante):
				conclusions = set(plugin(T, ante))
				if conclusions.issubset(set(fol.clauses)):
					qDash = plugin(T, cons)
					if all([Unify(x, qDash, {}) is None for x in fol.clauses + new]):
						if not set([False]).issubset(conclusions):
							new.append(qDash)
						Phi = Unify(qDash, A, {})
						if Phi == {}:
							if set([True]).issubset(conclusions):
								yield True
							if set([False]).issubset(conclusions):
								yield False
							yield True
						if Phi != None:
							yield Phi
		if not new:
			if str(A) in [str(x) for x in fol.clauses]:
				yield False
			if str(A)[0] == '~' and str(A)[1:] in [str(x) for x in fol.clauses]:
				yield False
			break
		for clause in new:
			fol.tell(clause)
	yield False

if __name__ == '__main__':
	
	fol = FOL()
	fol.tell(Rule('Human(Marcus)'))
	fol.tell(Rule('Pompeian(Marcus)'))
	fol.tell(Rule('Born(Marcus,40)'))
	fol.tell(Rule('Human(x)->Mortal(x)'))
	fol.tell(Rule('Erupted(Volcano,79)'))
	fol.tell(Rule('Erupted(Volcano,79) & Pompeian(x) -> Died(x,79)'))
	fol.tell(Rule('Mortal(x) & Born(x,t) & ((y - t) > 150) -> Dead(x,y)'))
	fol.tell(Rule('Alive(x,t) -> (~Dead(x,t))'))
	fol.tell(Rule('Dead(x,t) -> (~Alive(x,t))'))
	fol.tell(Rule('Died(x,t) & (y > t) -> Dead(x,y)'))
	fol.tell(Rule('Pompeian(x) -> Roman(x)'))
	fol.tell(Rule('Ruler(Caesar)'))
	fol.tell(Rule('Roman(x) & (~ Loyal(x,Caesar)) -> Hate(x,Caesar)'))
	fol.tell(Rule('Roman(x) & (~ Hate(x,Caesar))  -> Loyal(x,Caesar)'))
	fol.tell(Rule('Loyal(x,F(x))'))
	fol.tell(Rule('Human(x)->Person(x)'))
	fol.tell(Rule('Person(x) & Ruler(y) & TryAssassinate(x,y) -> (~Loyal(x,y))'))
	fol.tell(Rule('TryAssassinate(Marcus,Caesar)'))
	
	print fol.ask(Query('Alive(Marcus,60)'))
	print fol.ask(Query('TryAssassinate(x,Caesar)'))[x]
	print fol.ask(Query('Loyal(Marcus,Caesar)'))
	print fol.ask(Query('Ruler(x)'))[x]
	print fol.ask(Query('Erupted(Volcano,x)'))[x]
	print fol.ask(Query('Dead(Marcus,60)'))
	print fol.ask(Query('Hate(Marcus,Caesar)'))
	print fol.ask(Query('Alive(Marcus,35)'))

