#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from state import *
from helper import *
from api import *
from gui import *
import sys
import signal
import copy 
import os
import time
import winsound

#Aesthetics 
def signal_handler(sig, frame):
        print('Exiting from Keyboard interrupt.')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
sys.tracebacklimit = 5

def clear():
	if os.name == 'nt': 
		_ = os.system('cls') 
	else:
		_ = os.system('clear')
		
#End : Aesthetics

def GamePlay(g,SearchAlgorithm,diff):
	forfeit=[]
	sa = SearchAlgorithm(diff)
	sa2 = AlphaBeta('M')
	playerId = 1
	visited = set()
	gameState = g.getCurState()
	endGame = False
	
	numNodes = 0
	startTime = time.time()
	endTime = time.time()
	MemoryOfNode = 0
	MaxRecurse = 0
	nodesPerMicroSecond = 0
	
	f = open('Results'+str(randint(1,7))+'.txt','a')
	
	while True:
		g.activate(-1)
		decision = sa.gameStatus(g.getCurState())
		if decision != -1:
			if decision == 0:
				print "It's a draw match."
			elif decision == 1:
				print "Player 1 Wins."
			elif decision == 2:
				print "Player 2 Wins."
			endGame = True
			break
		print "It's the turn of : ",playerId
		if str((gameState.__hash__(),playerId)) not in visited:
			visited.add(str((gameState,playerId)))
			one,two = Util(g.getCurState().board)
			gameVal = 0
			if playerId == 1:
				gameVal = one*2-two*10
			else:
				gameVal = two*2-one*10
			print "Current Utility Value : ",(one,two,gameVal)
			g.Action = None
			winsound.Beep(2500, 500)
			if playerId == 2:
				g.setPlayer(2)
				g.activate(-1)
				print "Thinking..."
				action,results = sa.Decision(gameState,playerId)
				nodeMem,recurse,genNodes,timeElapsed = results
				MemoryOfNode = max(nodeMem,MemoryOfNode)
				MaxRecurse = max(MaxRecurse,recurse)
				nodesPerMicroSecond = max(nodesPerMicroSecond,genNodes/(timeElapsed*1000000))
				numNodes += genNodes
				
				g.move(action)
				g.activate(-1)
			else:	
				g.setPlayer(1)
				g.activate(1)
				action = None
				
				input = raw_input('Done?')
				action = g.getAction()
				
				# action,results = sa2.Decision(gameState,playerId)
				# g.move(action)
				
				g.activate(-1)
			gameState = g.curState		
			if action is None:
				print "Player ",playerId," gave up a turn."
				forfeit.append(playerId)
			else:
				forfeit.append(0)	
				if action[3] == 2:
					print "Player : ",playerId," takes coin..."
			if len(forfeit)>4 and forfeit[-1]>0 and forfeit[-3]>0 and forfeit[-1]==forfeit[-3]:
				print "Player : ",forfeit[-1]," forfeits...\n\n\n"
				break
			playerId = sa.opposite(playerId)
		else: #Player 1 i.e. user can intentionally repeat a state to declare win or draw.
			#Note : The game will of course never end if both players intentionally go back and forth between
			# set of states.
			print "Player : ",playerId," has repeated a move."
			f.write("Player : ",playerId," has repeated a move.")
			cs = g.getCurState()
			if cs.p1 > cs.p2:
				print "Player 1 Wins."
				f.write("Player 1 Wins.")
			elif cs.p1 < cs.p2:
				print "Player 2 Wins."
				f.write("Player 2 Wins.")
			else:
				print "The game ended in a Stale-Mate situation."
				f.write("It's a Draw.")
			break
	if not endGame:
		g.activate(-1)
		g.loop()
	else:
		endTime = time.time()
		print "Terminating in 2 seconds"
		g.pause(2)
		return numNodes,MemoryOfNode,MaxRecurse,nodesPerMicroSecond,endTime-startTime
		
	f.close()
		
def GameDriver():
	g = None
	size = (5,11)
	gameState = State(genInitBoard(size))
	lst = []
	results = []
	Mode = 'M' #Didn't provide user interface for this for easy evaluation purposes.
	##########################################################################
	#### E : Easy Mode : Depth is 4 for Minimax and 4 for AlphaBeta       ####
	#### M:  Medium Mode : Depth is 6 for Minimax and 6 for AlphaBeta     ####
	#### H : Hard Mode : Depth is 8 for Minimax and 8 for AlphaBeta       ####
	##########################################################################
	while True:
		clear()
		print "******************************************************************"
		print "****************** WELCOME TO HEXERS : THE GAME ******************"
		print "The User is Player 1. YOUR COLOR IS RED."
		print "Enter an option from the following: "
		print "<1> INITIALIZE AND DISPLAY A NEW BOARD."
		print "<2> PLAY A GAME USING MINIMAX."
		print "<3> PLAY A GAME USING ALPHABETA SEARCH."
		print "<4> SHOW RESULTS R1 THROUGH R12."
		print "<5> EXIT THE PROGRAM."
		print "******************************************************************"
		option = raw_input("Option Entry : ")
		print "******************************************************************"
		if option == "1":
			if g!=None:
				g.exit()
			g = GUI('Assignment 3 - Game Play')
			g.setCurState(gameState)
			g.setup()
			g.setPlayer(0)
			g.activate(-1)
			lst.append(1)
		elif option == "2":
			if len(lst)<1 or lst[-1]!=1:
				print "Please initialize a new board."
				if g!=None:
					g.exit() 
			else:
				lst.append(2)
				numNodes,MemoryOfNode,MaxRecurse,nodesPerMicroSecond,timeElapsed = GamePlay(g,Minimax,Mode)
				results = [numNodes,MemoryOfNode,MaxRecurse,timeElapsed,nodesPerMicroSecond]
				__replay__ = raw_input("Would you like to play another game [Y] or view results [R] or exit [N] :   ")
				if __replay__ == "N":
					print "You've chosen to exit the game."
					clear()
					print "Bye User!"
					if g!=None:
						print "Terminating in 3 seconds..."
						g.pause(3)
						g.exit()
					sys.exit(0)
				elif __replay__ == "Y":
					print "You've chosen to replay a game."
					if g!=None:
						g.exit()
				elif __replay__ == "R":
					print "You've chosen to view results of the game."
					print "--------------------------------------- RESULTS ---------------------------------------"
					print "Memory per node is ",MemoryOfNode," bytes."
					print "Maximum Depth of Recursion : ",MaxRecurse
					print "Number of nodes generated for the game : ",numNodes
					print "Number of nodes generated per microsecond : ",nodesPerMicroSecond
					print "Time Elapsed for the whole game (including delays by user) : ",timeElapsed," seconds."
					print "---------------------------------------------------------------------------------------"
		elif option == "3":
			if len(lst)<1 or lst[-1]!=1:
				print "Please initialize a new board."
				if g!=None:
					g.exit()
			elif len(results) < 5:
				print "Please play a game with Minimax algorithm first."
				if g!=None:
					g.exit()
					g = None
			else:
				lst.append(3)
				numNodes,MemoryOfNode,MaxRecurse,nodesPerMicroSecond,timeElapsed = GamePlay(g,AlphaBeta,Mode)
				results.append(numNodes)
				results.append((results[0]-results[5])/results[0])
				results.append(timeElapsed)
				__replay__ = raw_input("Would you like to play another game [Y] or view results [R] or exit [N] :   ")
				if __replay__ == "N":
					print "You've chosen to exit the game."
					clear()
					print "Bye User!"
					if g!=None:
						print "Terminating in 3 seconds..."
						g.pause(3)
						g.exit()
					sys.exit(0)
				elif __replay__ == "Y":
					print "You've chosen to replay a game."
					if g!=None:
						g.exit()
						g= None
				elif __replay__ == "R":
					print "You've chosen to view results of the game."
					print "--------------------------------------- RESULTS ---------------------------------------"
					print "Memory per node is ",MemoryOfNode," bytes."
					print "Maximum Depth of Recursion : ",MaxRecurse
					print "Number of nodes generated for the game : ",numNodes
					print "Number of nodes generated per microsecond : ",nodesPerMicroSecond
					print "Time Elapsed for the whole game (including delays by user) : ",timeElapsed," seconds."
					print "---------------------------------------------------------------------------------------"
		elif option == "4":
			if 2 in lst and 3 in lst:
				if results != None:
					if g != None:
						g.exit()
					g = GUI('Assignment 3 - Analysis Module')
					g.printResults(results)
					f = open('Results'+str(randint(1,7))+'.txt','a')
					f.write(str(results))
					f.close()
			else:
				print "Couldn't find any record of gameplay. Play a game."
		elif option == "5":
			clear()
			print "Bye User!"
			if g!=None:
				print "Terminating in 3 seconds..."
				g.pause(3)
				g.exit()
			sys.exit(0)
		print "Refreshing Menu in 3 seconds"
		time.sleep(1)
		print "Refreshing Menu in 2 seconds"
		time.sleep(1)
		print "Refreshing Menu in 1 second"
		time.sleep(1)
		
		
		
if __name__ == '__main__':
	GameDriver()
	try:
		f = open('Results.txt','w')
		f.close()
		GameDriver()
	except:
		print "Exiting from User Interrupt"
		sys.exit(0)
			
		
			