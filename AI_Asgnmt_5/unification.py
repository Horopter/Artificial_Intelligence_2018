from helper import *

def Unify(x, y, t={}):
	if t is None:
		return None
	elif x == y:
		return t
	elif IsVar(x):
		return UnifyVar(x, y, t)
	elif IsVar(y):
		return UnifyVar(y, x, t)
	elif isinstance(x, Stmt) and isinstance(y, Stmt):
		return Unify(x.operands, y.operands, Unify(x.operator, y.operator, t))
	elif isinstance(x, str) or isinstance(y, str):
		return None
	elif isinstance(x, (list,tuple)) and isinstance(y, (list,tuple)) and len(x) == len(y):
		if not x:
			return t
		return Unify(x[1:], y[1:], Unify(x[0], y[0], t))
	else:
		return None


def UnifyVar(var, x, t):
	if var in t:
		return Unify(t[var], x, t)
	elif x in t:
		return Unify(var, t[x], t)
	elif OccurCheck(var, x, t):
		return None
	else:
		s2 = t.copy()
		s2[var] = x
		return s2


def subst(a, b):
	if isinstance(b, list):
		return [subst(a, instx) for instx in b]
	elif isinstance(b, tuple):
		return tuple([subst(a, instx) for instx in b])
	elif not isinstance(b, Stmt):
		return b
	elif b.operator == '-':
		p,q = subst(a,b.operands[0]),subst(a,b.operands[1])
		if type(p) in (int,float) and type(q) in (int,float):
			return p-q
	elif b.operator == '+':
		p,q = subst(a,b.operands[0]),subst(a,b.operands[1])
		if type(p) in (int,float) and type(q) in (int,float):
			return p+q
	elif b.operator == '>':
		p,q = subst(a,b.operands[0]),subst(a,b.operands[1])
		if type(p) in (int,float) and type(q) in (int,float):
			return p>q
	elif IsVar(b.operator):
		return a.get(b, b)
	else:
		if len(b.operands)==0 and b.operator in [str(x) for x in a.keys()]:
			return a[Stmt(b.operator)]
		return Stmt(b.operator, *[subst(a, oper) for oper in b.operands])
	

def OccurCheck(var, x, t):
	if var == x:
		return True
	elif IsVar(x) and x in t:
		return OccurCheck(var, t[x], t)
	elif isinstance(x, (list, tuple)):
		return First(a for a in x if OccurCheck(var, a, t))
	elif isinstance(x, Stmt):
		return (OccurCheck(var, x.operator, t) or OccurCheck(var, x.operands, t))
	else:
		return False