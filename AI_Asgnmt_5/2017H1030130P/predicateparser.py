#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

class PredicateParser:
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
	
	def parseLine(self,s):
		s = s.replace('\n','')
		predicates = []
		pred, description = self.split(s,':')
		lst = self.getFunction(pred)
		print "Function Name : ",lst[0]
		print "Function Args : ",lst[1:]
		print "Function Description : ",description
		return lst
	
	def parse(self,f):
		predicates = []
		with open(f,"r") as fl:
			line = fl.readline()
			while line:
				p = self.parseLine(line)
				predicates.append(p)
				line = fl.readline()
		return predicates