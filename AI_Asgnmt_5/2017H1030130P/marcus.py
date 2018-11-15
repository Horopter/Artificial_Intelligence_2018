#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from ruleparser import RuleParser
from predicateparser import PredicateParser
from api import *
from helper import *
class Marcus:
	def __init__(self):
		self.lst = 	[
						'Alive(Marcus,x) & Now(x)',
						'TryAssassinate(x,Caesar)',
						'Loyal(Marcus,Caesar)',
						'Ruler(x)',
						'Erupted(Volcano,x)',
						'Dead(Marcus,60)',
						'Hate(Marcus,Caesar)',
						'Alive(Marcus,35)'
					]
	def DefineProblem(self,predf,rulef):
		self.fol = FOL()
		self.pp = PredicateParser()
		#self.pp.parse(predf)
		self.rp = RuleParser()
		rules = self.rp.parse(rulef)
		
		for r in rules:
			self.fol.tell(Rule(r))
			
	def Query(self,q):
		ans = self.fol.ask(Query(self.lst[q]))
		if type(ans) == dict:
			return ans[ans.keys()[0]]
		else:
			return ans

