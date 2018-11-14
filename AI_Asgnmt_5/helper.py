import keyword,re,collections

def IsId(candidate):
	is_not_keyword = candidate not in keyword.kwlist
	pattern = re.compile(r'^[a-z_][a-z0-9_]*$', re.I)
	matches_pattern = bool(pattern.match(candidate))
	return is_not_keyword and matches_pattern

def IsTerm(t):
	return (isinstance(t, str) and t[0].isalpha()) or (t in ['~','>'])

def IsVar(x):
	return isinstance(x, Stmt) and not x.operands and x.operator[0].islower()
	
def Vars(t):
	y = {x for x in statements(t) if IsVar(x)}
	#print "Varsy : ",y
	return y
	
def First(iterable, default=None):
	try:
		return iterable[0]
	except IndexError:
		return default
	except TypeError:
		return next(iterable, default)

class Stmt(object):
	def __init__(self, operator, *operands):
		self.operator = str(operator)
		self.operands = operands

	def __and__(self, r):
		return Stmt('&', self, r)
		
	def __or__(self, r):
		if isinstance(r, (Stmt, int, float, complex)):
			return Stmt('|', self, r)
		else:
			return Partial(r, self)
	
	def __invert__(self):
		return Stmt('~', self)
			
	def __add__(self, r):
		print self,r
		return Stmt('+', self, r)

	def __sub__(self, r):
		return Stmt('-', self, r)
		
	def __gt__(self, r):
		return Stmt('>', self, r)
		
	def __call__(self, *operands):
		if not self.operands:
			return Stmt(self.operator, *operands)
			
	def __eq__(self, r):
		return (isinstance(r, Stmt) and self.operator == r.operator and self.operands == r.operands)

	def __hash__(self):
		return hash(self.operator) ^ hash(self.operands)

	def __repr__(self):
		operator = self.operator
		operands = [str(o) for o in self.operands]
		if IsId(operator):
			return '{}({})'.format(operator, ', '.join(operands)) if operands else operator
		elif len(operands) == 1:
			return operator + operands[0]
		else:
			return '(' + (' ' + operator + ' ').join(operands) + ')'
			
def statements(x):
	yield x
	if isinstance(x, Stmt):
		for o in x.operands:
			se = statements(o)
			for y in se:
				yield y

class Partial:
	def __init__(self, operator, f):
		self.operator, self.f = operator, f

	def __or__(self, r):
		return Stmt(self.operator, self.f, r)
		
class defaultkeydict(collections.defaultdict):
	def __missing__(self, key):
		self[key] = result = self.default_factory(key)
		return result

def evaluatorFn(x):
	x = x.replace('->', '|' + repr('->') + '|')
	return x
		
def Rule(x):
	if isinstance(x, str):
		y = eval(evaluatorFn(x), defaultkeydict(Stmt))
		return y
	else:
		return x
		
def Query(x):
	return Rule(x)