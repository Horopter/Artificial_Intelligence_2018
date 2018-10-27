from state import *
from api import *

def drive(): 
	st = State(4)
	stk = []
	node = dfs(st,stk)
	node.printMe()
	
if __name__ == '__main__':
	drive()