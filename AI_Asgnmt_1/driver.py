#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from api import *
from gui import *
from analysis import graph
import sys
import os.path

def worker(size,pct,goal,algos,showProgress):
	isq = None
	screen = None
	options=[]
	analysis=[]
	maxdepth = 0
	while(1):
		cmd = raw_input("Algorithm 1 : DFS.\nAlgorithm 2 : IDS.\nEnter an option.\nFor defining initial grid and initial state, enter 1.\nFor running the first algorithm, enter 2.\nFor running second algorithm, enter 3.\nFor starting analysis module, enter 4.\nTo exit the program, enter 5.\n-> ")
		try:
			cmd = int(cmd)
		except:
			print "Runtime exception. Please proceed to debug."
			sys.exit(0)

		if cmd == 1:
			if cmd in options:
				print "Grid was initialized already."
				continue
			check = 0
			while isq is None and check < 10:
				isq = getInitSquares(size,pct,goal,showProgress)
				check += 1
			if check == 10:
				print "Initial squares not sufficient for goal squares.\nExiting now...\nBye!"
				sys.exit(0)
			if isq is not None:
				positions = [i for i in range(len(isq)) if isq[i]]
				raw = [i for i in range(len(isq))]
				screen = getWindow()
				partition(screen)
				for i in range(len(algos)):
					drawGrid('grey',raw,size,screen,i+1,2)
					drawGrid('blue',positions,size,screen,i+1,3)
				options.append(1)

		elif cmd == 2:
			if cmd in options:
				print "This algorithm was run already."
				continue
			if (1 in options):
				res = runAlgorithm(size,goal,algos[cmd-2],isq,showProgress)
				actions = res[2]
				maxdepth = res[3]
				drawGrid('red',actions,size,screen,cmd-1,3)
				textit(algos[cmd-2],res[5],sys.getsizeof(res[0]),res[4],res[2],len(res[2]),res[6],cmd-1)
				analysis.append([algos[cmd-2],res[4]*sys.getsizeof(res[0])])
				options.append(cmd)
			else:
				print "Please define initial state."

		elif cmd == 3:
			if cmd in options:
				print "This algorithm was run already."
				continue
			if 2 not in options:
				print "Run the first algorithm first."
				continue
			if maxdepth > 10:
				print "DFS returned a solution with depth > 10, we would not recommend running IDS."
				print "Please choose a lower percentage of coverage or higher number of squares in goal state on next run."
				print "Would you like to run IDS?"
				agreement = raw_input("Enter Y/N: ")
				if agreement == "Y":
					print "You've chosen to run IDS algorithm."
					if (1 in options):
						res = runAlgorithm(size,goal,algos[cmd-2],isq,showProgress)
						actions = res[2]
						drawGrid('red',actions,size,screen,cmd-1,3)
						textit(algos[cmd-2],res[5],sys.getsizeof(res[0]),res[4],res[2],len(res[2]),res[6],cmd-1)
						analysis.append([algos[cmd-2],res[4]*sys.getsizeof(res[0])])
						options.append(cmd)
					else:
						print "Please define initial state."
				else:
					print "You've chosen not to run IDS. Exiting Module now...\nBye!"
					sys.exit(0)
			else:
				if (1 in options):
					res = runAlgorithm(size,goal,algos[cmd-2],isq,showProgress)
					actions = res[2]
					drawGrid('red',actions,size,screen,cmd-1,3)
					textit(algos[cmd-2],res[5],sys.getsizeof(res[0]),res[4],res[2],len(res[2]),res[6],cmd-1)
					analysis.append([algos[cmd-2],res[4]*sys.getsizeof(res[0])])
					options.append(cmd)
				else:
					print "Please define initial state."
		elif cmd == 4:
			if cmd in options:
				print "Analysis was performed already."
				continue
			if (1 in options) and (2 in options) and (3 in options):
				if analysis[1][1] == analysis[0][1]:
					publish(analysis,0)
				elif analysis[1][1] > analysis[0][1]:
					publish(analysis,1)
				else:
					publish(analysis,-1)
				print str(size)+"_"+str(pct)+"_"+str(goal)+"_dfs_analysis.pkl"
				if os.path.isfile(str(size)+"_"+str(pct)+"_"+str(goal)+"_dfs_analysis.pkl") and os.path.isfile(str(size)+"_"+str(pct)+"_"+str(goal)+"_ids_analysis.pkl"):
					t = graph(pct,goal,size)
					a1,a2 = t
					inform(a1,a2)
				print "Stats printed. Please exit the screen."
			else:
				print "Please run both the algorithms at least once."
		else:
			print "Exiting the console. Bye!" 
			sys.exit(0)
	if screen is not None:
		runLoop()

def terminalDriver():
	size = raw_input("Enter the size of the grid (2 to 8) : ")
	try:
		size = int(size)
		if size < 2 or size > 8:
			print "The given program doesn't support given size. Exiting the program now. \nBye!"
			sys.exit(0)
	except:
		print "It's not a valid number. Exiting the program now. \nBye!"
		sys.exit(0)

	pct = raw_input("Enter the percentage of the grid to be covered/tiled with matchsticks (0 to 100): ")
	try:
		pct = float(pct)
		if pct < 0 or size > 100:
			print "The given percentage is not a valid number. Exiting the program now. \nBye!"
			sys.exit(0)
	except:
		print "It's not a valid float number. Exiting the program now. \nBye!"
		sys.exit(0)

	goal = raw_input("Enter the number of squares you wish to be in the goal state : ")
	try:
		goal = int(goal)
		if (pct*size*size//100) < goal:
			print "We can't get initial squares more than goal specified with given size and percentage of coverage. Exiting the program now. \nBye!"
			sys.exit(0)
	except:
		print "It's not a number. Exiting the program now. \nBye!"
		sys.exit(0)

	showProgress = raw_input("Do you wish to view the progress on terminal in textual format? (Y/N) : ")
	if showProgress is "Y":
		showProgress = True
		print "You've chosen to view the progress in textual format on the terminal."
	elif showProgress is "N":
		showProgress = False
		print "You've chosen to hide the progress from displaying on the terminal screen."
	else:
		print "Invalid option. Exiting the program now. \nBye!"
		sys.exit(0)
	return (size,pct,goal,showProgress)

if __name__ == "__main__":
	res = terminalDriver()
	size,pct,goal,showProgress = res
	algos=['dfs','ids']
	worker(size,pct,goal,algos,showProgress)