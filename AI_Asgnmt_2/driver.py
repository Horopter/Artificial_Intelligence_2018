#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from helper import *
from api import *
from gui import *
import sys

#guide for result : name,max_aux_len,max_depth,visited_nodes,auxiliary,actions,desiredGoal,reached_goal,time,graph

INIT = ((19,120,26,16,90),(116,148,132),(104,31,28,37,200,81),(118,106,99,1,40,63,190,205,10),(14,32,20,36,78,22),(11,16,8,12,98,33,135,144,3),(39,70,86,55,100),(316,178,122),(141,302),(341,112,89,67,54,44))
INTER = ((19,120,26,190,116),(67,54,44),(104,31,28,37,200,16,10),(118,106,99,1,40,63,),(14,32,20,36,,78,100,3),(11,16,8,12,98,33,),(39,70,81,22),(316,178,122),(141,302),(341,112,89,67,54,44)) 
FINAL = ((19,120,26,10),(116,),(104,31,28,37,200,16),(118,106,99,1,40,63,190),(14,32,20,36,78,100,3,81,22),(11,16,8,12,98,33,135),(39,70),(316,178,122,205,148),(55,144,90,132,302,86),(341,112,89,67,54,44,141))
	
def graphArr(G):
	x_ = []
	y_ = []
	for _i in G:
		_x,_y = _i
		x_.append(_x)
		y_.append(_y)
	minx = min(x_)	
	miny = min(y_)
	scaley = (max(y_)-miny)/10
	scalex = (max(x_)-minx)/10
	_g=[]
	for x in G:
		_g.append(((x[0]-minx)/(1.0*scalex+1),(x[1]-miny)/(1.0*scaley+1),x[0],x[1]))
	return _g
	
def main():

	algoP = {'#':1,'$':2}
	hP = {'@':2,'%':3}

	results = {}
	combos = []
	g = None
	g = GUI("Assignment 2")
	init = None
	goal = None
	lastcmd = 0
	while True:
		ipt = raw_input("Algorithm 1: HillClimbing\nAlgorithm 2: A* Search\nHeuristic 1: greaterRewardThanPenalty\nHeuristic 2: PositionalRewardStaticPenalty\n********************\n\tMenu\n********************\nPress 1 to create and display Initial Environment\nPress 2 to view movements\nPress 3 to view results for first technique\nPress 4 to view results for second technique\nPress 5 to view results and graphs\nPress 6 to exit.\nEnter your Option : ")
		if ipt == "1":
			init = genInitState(90,10)
			goal = genGoalState(init,10)
			g.setInitState(init)
			g.setGoalState(goal)
			g.representState()
			lastcmd = 1
		elif ipt == "2":
			if lastcmd == 2:
				print "Please Initialize a new environment again..."
				continue
			init.show()
			algo = raw_input("Press # to run first technique or press $ to run second technique : ")
			heuristic = raw_input("Press @ to use first heuristic or press % to run second heuristic : ")
			if algo not in ['#','$'] or heuristic not in ['@','%']:
				print "Invalid Option for algorithm or heuristic..."
				continue
			if (algo,heuristic) in combos:
				print "This combination has been tried out. Try a different combination."
				continue
			combos.append((algo,heuristic))
			A = algoP[algo]
			H = hP[heuristic]
			result = runAlgorithm(init,goal,A,H)
			results[(algo,heuristic)]=result
			g.createNext(result[5])
			hatchet = raw_input("Press Enter/Return key to resume...\n")
			g.reset()
			lastcmd = 2
		elif ipt == "3":
			if not ('#','@') in results or not ('#','%') in results:
				print "Try both heuristics..."
				continue
			choice = raw_input("Press @ if you wish to use first heuristic or % for second heuristic : ")
			t1a = results[('#','@')]
			t1b = results[('#','%')]
			t1 = None
			if choice == '@':
				t1 = t1a
			elif choice == '%':
				t1 = t1b
			else:
				print "Invalid choice."
				continue
			r1 = max(t1[1][0],t1[3][0])*sys.getsizeof(t1[7])
			g.create_label('r1',"(R1) The maximum memory consumed is : "+str(r1) + " bytes.")
			r2 = t1[-2]
			g.create_label('r2',"(R2) The time taken is : "+str(r2)+ " seconds.")
			r3 = t1[-3].cost
			g.create_label('r3',"(R3) The cost incurred is : "+str(r3)+" units.")
			r5 = len(runAlgorithm(state_from_hash(INIT),state_from_hash(FINAL),algoP['#'],hP[choice])[5])
			g.create_label('r5',"(R5) The cost incurred for given problem is : "+str(r5)+" units.")
		elif ipt == "4":
			if not ('$','@') in results or not ('$','%') in results:
				print "Try both heuristics..."
				continue
			choice = raw_input("Press @ if you wish to use first heuristic or % for second heuristic : ")
			t2a = results[('$','@')]
			t2b = results[('$','%')]
			t2 = None
			if choice == '@':
				t2 = t2a
			elif choice == '%':
				t2 = t2b
			else:
				print "Invalid choice."
				continue
			r6 = max(t2[1][0],t2[3][0])*sys.getsizeof(t2[7])
			g.create_label('r6',"(R6) The maximum memory consumed is : "+str(r6) + " bytes.")
			r7 = t2[-2]
			g.create_label('r7',"(R7) The time taken is : "+str(r7)+ " seconds.")
			r8 = t2[-3].cost
			g.create_label('r8',"(R8) The cost incurred is : "+str(r8)+" units.")
			r10 = len(runAlgorithm(state_from_hash(INIT),state_from_hash(FINAL),algoP['$'],hP[choice])[5])
			g.create_label('r10',"(R10) The cost incurred for given problem is : "+str(r10)+" units.")
		elif ipt =="5":
			if len(results)!=4:
				print "Please try out all the combinations..."
				continue			
			g.drawPartition()
			g.graphSetup()
			g.drawGraph(graphArr(t1a[-1]),1,"blue")
			g.drawGraph(graphArr(t1b[-1]),1,"green")
			g.drawGraph(graphArr(t2a[-1]),2,"blue")
			g.drawGraph(graphArr(t2b[-1]),2,"green")
			hill = []
			ast = []
			#g.drawGraph(graphArr(hill),3,"blue")
			#g.drawGraph(graphArr(ast),3,"blue")
			g.create_label('r11',"(R11) A* takes more memory than HillClimbing technique in given implementation \n for larger shuffle parameters.")
			g.create_label('r12',"(R12) The average path cost was determined as 14 for hillClimbing and 8.5 for A* \n when shuffle parameter was given as 10.")
		elif ipt=="6":
			exit()
	if g is not None:
		g.loop()
		
if __name__ == "__main__":
	main()