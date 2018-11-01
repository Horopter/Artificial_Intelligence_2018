#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from api import MagicSquare
from gui import GUI

def confirmation(s):
	if s=="3":
		return None
	return s=="1"
	
def driver():
	inputs = []
	n = raw_input("Enter a number : ")
	n = int(n)
	r = {}
	g = None
	while True:
		valueOrder,forwardCheck,constraintProp = False,False,False
		choice = raw_input("Enter \n 1 for DFS+BT \n 2 for DFS+BT+ConProp \n 3 to Exit \n ->  ")
		if choice != "3":
			valueOrder = raw_input("Enter 1 to use MRV + Degree heuristic \nor 2 to use default ordering (1,2,3...) \nor 3 to use Siam heuristic : ")
			valueOrder = confirmation(valueOrder)
		else:
			exit()
			
		if choice == "2":
			forwardCheck = raw_input("Enter 1 to use forward check or 2 to NOT use forward check : ")
			constraintProp = raw_input("Enter 1 to use AC3 algorithm to reduce domains at each step and 2 otherwise : ")
			forwardCheck = confirmation(forwardCheck)
			constraintProp = confirmation(constraintProp)
			
		inputs.append((n,valueOrder,forwardCheck,constraintProp))
		
		if g!= None and isinstance(g,GUI):
			g.exit()
			
		g = GUI("Assignment - 4 :: Number of squares : "+ str(n))
		g.prepGrid(n)
		x = MagicSquare(n,valueOrder, forwardCheck, constraintProp)
		sols,nodeSize,numNodes,maxDepth,duration = x

		if (n,False,False,False) in inputs and (n,True,False,False) in inputs and (n,True,True,False) in inputs:
			r[5] = numNodes[0]
			r[6] = (r[0]-r[5])*1.0/r[0]
			r[7] = duration
			g.printResults(r)
		elif (n,False,False,False) in inputs and (n,True,False,False) in inputs:
			r[4] = numNodes[0]
		elif (n,False,False,False) in inputs:
			r[0],r[1],r[2],r[3] = numNodes[0],nodeSize[0],maxDepth[0],duration
		
		g.putValues(n,sols[0])
		
	
	
if __name__ == "__main__":
	driver()