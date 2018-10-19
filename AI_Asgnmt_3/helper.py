#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from random import *
def genEmptyBoard(size):
	n = size[0]
	m = size[1]
	board = []
	for i in range(0,n):
		lst = []
		for j in range(0,m):
			lst.append(-2)
		board.append(lst)
	for i in range(0,n):
		d = abs(n/2 - i)
		for j in range(0,d):
			board[i][j]=-1
			board[i][m-j-1]=-1
		turn = 0
		for j in range(d,m-d):
			board[i][j]=turn
			if turn == 0:
				turn = -1
			elif turn == -1:
				turn = 0
	return board
	
def fillBoard(board,size,cntCoin):
	q = (size[1]+1)/2
	p = size[0]/2
	room = q*(2*p+1)-p*(p+1)
	if cntCoin > room/2:
		raise ValueError('We can\'t fit given number of coins for both players.')
	zrs = []
	for i in range(0,size[0]):
		for j in range(0,size[1]):
			if board[i][j]==0:
				zrs.append((i,j))
				
	for i in range(0,cntCoin):
		r = -1
		while r == -1:
			r = randint(0,room-1)
			x,y = zrs[r]
			if board[x][y]==0:
				board[x][y]=1
			else:
				r = -1
	for i in range(0,cntCoin):
		r = -1
		while r == -1:
			r = randint(0,room-1)
			x,y = zrs[r]
			if board[x][y]==0:
				board[x][y] = 2
			else:
				r = -1
				
def genInitBoard(size):
	board = genEmptyBoard(size)
	fillBoard(board,size,10)
	return board

def writeBoard(board,size):
	for i in range(0,size[0]):
		for j in range(0,size[1]):
			print board[i][j]," ",
		print
				
def Util(board):
	cnt13,cnt11,cnt23,cnt21 = 0,0,0,0
	size = (len(board),len(board[0]))
	for i in range(size[0]):
		for j in range(size[1]):
			if board[i][j] == 1:
				if count(board,i,j,size)==3:
					cnt13 += 3
				else:
					cnt11 += 1
			elif board[i][j] == 2:
				if count(board,i,j,size)==3:
					cnt23 += 3
				else:
					cnt21 += 1
	score1,score2 = (cnt13+cnt11),(cnt23+cnt21)
	return score1,score2
	
def printAction(node,value):
	if node is not None and node.utility == value:
		print "Action : ",node.action," with a value of ",value
	for x in node.child_nodes:
		if x is not None and x.utility == value:
			printAction(x,value)
				
def count(lst,x,y,size):
	l = [(-1,1),(0,2),(1,1),(1,-1),(0,-2),(-1,-1)]
	cnt = 0
	for a in l:
		ax,ay = a
		if x+ax>-1 and y+ay>-1 and (x+ax<size[0] and y+ay<size[1] and lst[x+ax][y+ay] != -1) or (x+2*ax<size[0] and y+2*ay<size[1] and lst[x+2*ax][y+2*ay] != -1):
			cnt += 1
	return cnt
				
if __name__ == '__main__':
	size = 5
	board = genInitBoard(size)
	writeBoard(board,size)
	
	