#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from random import *
from helper import *
import copy
import pickle

def tileGrid(grid,size,target):
	count = 0
	free = size*size
	g = copy.deepcopy(grid)
	while count < target:
		if target - count > free:
			grid = g
			return False
		face = randint(0,size*size-1)
		x,y = face/size,face%size
		if grid[x][y] is 0:
			ans = False
			while not ans:
				r = randint(1,size)
				if free < r*r:
					continue
				if x+r<=size and y+r<=size:
					res = True
					for i in range(x,x+r):
						for j in range(y,y+r):
							if grid[i][j] is not 0:
								res = False
					if res:
						for i in range(x,x+r):
							for j in range(y,y+r):
								grid[i][j]=r
						count += 1
						free -= r*r
						ans = True
	if count > target:
		grid = g
		return False
	return True

def goalState(size,target):
	grid = genGrid(size)
	res = False
	while not res:
		if isFilled(grid,size):
			grid = genGrid(size)
		if tileGrid(grid,size,target):
			lst = genTuple(size)
			fillTuple(grid,size,lst)
			sq = countSquares(size,lst)
			res = (sq == target)
			if sq > target:
				grid = genGrid(size)
	return grid

def genGoals(size,squares=4):
	print "Generating goal states for ",size,"x",size," mesh."
	for j in range(1,squares):
		print "With ",j," number of squares..."
		actual = []
		done = False
		while not done:
			prev = len(actual)
			for i in range(0,2*prev+1):
				g = goalState(size,j)
				if g not in actual and g != genGrid(size):
					actual.append(g)
			done = (len(actual) == prev)
		f = open(str(size)+"_"+str(j)+".pkl","wb")
		pickle.dump(actual,f)
		f.close()
		print "Possibilities found:",len(actual)

if __name__ == "__main__":
	for i in range(2,7):
		genGoals(i)
	

