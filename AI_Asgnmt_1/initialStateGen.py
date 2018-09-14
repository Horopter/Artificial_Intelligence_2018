#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from random import *
from helper import *
import copy

def getCoverage(grid,size,tuplet):
	coverage = 0
	for x in range(0,size):
		for y in range(0,size):
			item = x*size+y
			if grid[x][y] is not 0:
				coverage += 1
			else:
				top = size * (item/size) + item + (item/size)
				right = (size+1) * (item/size) + item + size + 1
				left = (size+1) * (item/size) + item + size
				bottom = size * (item/size) + item + (item/size) + 2*size + 1
				if top>=0 and top < size and left>=0 and left < size and right>=0 and right < size and bottom>=0 and bottom<size:
					if tuplet[top] and tuplet[right] and tuplet[left] and tuplet[bottom]:
						coverage +=1 
	return coverage

def putFace(grid,size,coverage):
	while coverage > 0:
		face = randint(0,size*size-1)
		x,y = face/size,face%size
		if grid[x][y] is 0:
			ans = False
			while not ans:
				r = randint(1,size)
				if coverage < r*r:
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
						coverage-= r*r
						ans = True

def getGrid(size,target):
	grid = genGrid(size)
	res = False
	while not res:
		putFace(grid,size,target)
		lst = genTuple(size)
		fillTuple(grid,size,lst)
		coverage = getCoverage(grid,size,lst)
		res = (coverage == target)
	return lst

def initStateGen(size,pct):
	sq = size*size
	target = round((pct*sq)/100)
	return getGrid(size,target)

if __name__ == "__main__":
	print initStateGen(4,48)

