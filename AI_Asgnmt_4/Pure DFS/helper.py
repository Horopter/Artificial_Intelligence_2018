import math

def sqrt(num):
	return int(math.sqrt(num))

def rowSum(lst,size):
	side = sqrt(size)
	rows = []
	for i in range(side):
		sum = 0
		for j in range(side):
			sum += lst[i*side+j]
		rows.append(sum)
	return rows
		
def colSum(lst,size):
	side = sqrt(size)
	cols = []
	for i in range(side):	
		sum = 0
		for j in range(side):
			sum += lst[i+j*side]
		cols.append(sum)
	return cols

def dgnlSum(lst,size):
	side = sqrt(size)
	dgnls = []
	sum = 0
	for i in range(side):
		sum += lst[i*side+i]
	dgnls.append(sum)
	
	sum = 0
	for i in range(side):
		sum += lst[i*side+(side-1-i)]
	dgnls.append(sum)
	return dgnls
	
def allSame(lst):
	if len(lst) < 1:
		return False
	elem = lst[0]
	for i in lst:
		if i != elem:
			return False
	return True
	
def allEqual(lst):
	size = len(lst)
	
	if size == 0 or lst[-1] == 0:
		return False
		
	r = rowSum(lst,size)
	c = colSum(lst,size)
	d = dgnlSum(lst,size)
	
	if allSame(r) and allSame(c) and allSame(d):
		if r[0]==c[0] and c[0]==d[0]:
			if r[0] != 0:
				return True
				
	return False