#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

def genGrid(number):
	lst = []
	for i in range(0,number):
		l = []
		for j in range(0,number):
			l.append(0)
		lst.append(l)
	return lst

def genTuple(size):
	lst = []
	for i in range(0,2*size*(size+1)):
		lst.append(False)
	return lst

def fillTuple(grid,size,tuplet):
	top=0
	left=0
	right=0
	bottom=0
	myhash = genTuple(size*size)
	for x in range(0,size):
		for y in range(0,size):
				r = grid[x][y]
				if r is not 0 and not myhash[x*size+y]:
					for i in range(0,r):
						for j in range(0,r):
							myhash[(x+i)*size+y+j]=True
					for i in range(0,r):
						item = x*size + y + i
						top = (size+1) * (item/size) + item
						tuplet[top]=True

						item = (x+i)*size+y+r-1
						right = (size+1) * (item/size) + item + size + 1
						tuplet[right]=True

						item = (x+i)*size+y
						left = (size+1) * (item/size) + item + size
						tuplet[left]=True

						item = (x+r-1)*size + y + i
						bottom = (size+1) * (item/size) + item + 2*size + 1
						tuplet[bottom]=True

def horizontal(num,size):
	return num%(2*size+1) < size

def vertical(num,size):
	return num%(2*size+1) >= size

def init_tour(index,radius,size,tuplet):
	res = True
	L = len(tuplet)
	for i in range(0,radius):#top
		item = index+i
		if not (item < L and tuplet[item] and horizontal(item,size)):
			return False
	for i in range(0,radius):#left
		item = index + size + i*(2*size+1)
		if not (item < L and tuplet[item] and vertical(item,size)):
			return False
	for i in range(0,radius):#right
		item = index + size + i*(2*size+1) + radius
		if not (item < L and tuplet[item] and vertical(item,size)):
			return False
	for i in range(0,radius):#bottom
		item = index+ radius*(2*size+1)+i
		if not (item < L and tuplet[item] and horizontal(item,size)):
			return False
	return True

def countSquares(size,tuplet):
	L = len(tuplet)
	count = 0
	for j in range(0,L):
		if horizontal(j,size):
			for i in range(1,size+1):
				if init_tour(j,i,size,tuplet):
					count += 1
					break
	return count

def isFilled(grid,size):
	for x in range(0,size):
		for y in range(0,size):
			if grid[x][y] is 0:
				return False
	return True