#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

import copy

class RuleParser:
	def split(self,s,sep=' '):
		if isinstance(s,str):
			return s.split(sep)
		
	def getFunction(self,fn):
		if '(' in fn:
			fnName, rest = self.split(fn,'(')
			arglist, empty = self.split(rest,')')
			args = self.split(arglist,',')
			fnl = [fnName]
			fnl.extend(args)
			return fnl
		else:
			fnl = [fn]
			return fnl
		
	def getFunctionList(self,lst):
		fnlst = []
		for fn in lst:
			fnlst.append(self.getFunction(fn))
		return fnlst
		
	def getTuple(self,t):
		s = ','.join(t)
		s = '('+s+')'
		if s!='()':
			return s
		else:
			return ''
		
	def parseQuantifiers(self,s):
		everybucket = set()
		existsbucket = set()
		lst = self.split(s)
		for i in range(0,len(lst),2):
			if 'For_every' in lst[i]:
				everybucket.add(lst[i+1])
			elif 'There_exists' in lst[i]:
				existsbucket.add(lst[i+1])
		return everybucket,existsbucket

	def parseLine(self,s):
		s = s.replace('\n','')
		rules = []
		quantifiers,rest='',''
		everybucket,existsbucket = [],[]
		
		if ':' not in s:
			quantifiers,rest = '',s
		else:
			quantifiers,rest = self.split(s,':')		
			everybucket,existsbucket = self.parseQuantifiers(s) 
		antecedent,consequent = '',''
		if '->' in rest:
			antecedent, consequent = self.split(rest,'->')
		else:
			antecedent, consequent = rest,''
			
		antTerms = self.split(antecedent,' and ')
		Afns = self.getFunctionList(antTerms)
		
		antTermsMod = []
		for afn in Afns:
			name = afn[0]
			args = afn[1:]
			if len(existsbucket) > 0:
				fargs = []
				for arg in args:
					if arg in list(existsbucket):
						rest = copy.deepcopy(args)
						rest.remove(arg)
						fargs = copy.deepcopy(args)
						fargs = [x.replace(arg,'F'+self.getTuple(rest)) for x in fargs]
				if len(fargs)>0:
					antTermsMod.append(name + self.getTuple(fargs))
			else:
				antTermsMod.append(name + self.getTuple(args))
			
		consTerms = self.split(consequent,' or ')
		Cfns = self.getFunctionList(consTerms)
		
		consTermsMod = []
		for cfn in Cfns:
			name = cfn[0]
			args = cfn[1:]
			if len(existsbucket) > 0:
				fargs = []
				for arg in args:
					if arg in list(existsbucket):
						rest = copy.deepcopy(args)
						rest.remove(arg)
						fargs = copy.deepcopy(args)
						fargs = [x.replace(arg,'F'+self.getTuple(rest)) for x in fargs]
				if len(fargs)>0:
					consTermsMod.append(name + self.getTuple(fargs))
			else:
				consTermsMod.append(name + self.getTuple(args))
		
		ant = " & ".join(antTermsMod)
		for c in consTerms:
			rule = ant
			dupe = copy.deepcopy(consTerms)
			dupe.remove(c)
			for d in dupe:
				rule = rule + ' & ' + ' [~ ' + d + ' ] '
			if rule != '' and c != '':
				rule = rule + ' -> ' + c
			rule = rule.replace('[','(')
			rule = rule.replace(']',')')
			rules.append(rule)
		return rules
		
	def parse(self,f):
		rules = []
		with open(f,"r") as fl:
			line = fl.readline()
			while line:
				p = self.parseLine(line)
				rules.extend(p)
				line = fl.readline()
		return rules
