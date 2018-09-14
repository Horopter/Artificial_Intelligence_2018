#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

from api import *
import pickle
import os.path

def runRandom(pct,fsq,size,ret=False):
	i = size
	j = pct
	k = fsq
	A1 = []
	A2 = []
	if ret and (os.path.isfile(str(i)+"_"+str(j)+"_"+str(k)+"_dfs_analysis.pkl") or os.path.isfile(str(i)+"_"+str(j)+"_"+str(k)+"_ids_analysis.pkl")):
		A1 = pickle.load(open(str(i)+"_"+str(j)+"_"+str(k)+"_dfs_analysis.pkl","rb"))
		A2 = pickle.load(open(str(i)+"_"+str(j)+"_"+str(k)+"_ids_analysis.pkl","rb"))
	elif not (os.path.isfile(str(i)+"_"+str(j)+"_"+str(k)+"_dfs_analysis.pkl") or os.path.isfile(str(i)+"_"+str(j)+"_"+str(k)+"_ids_analysis.pkl")):
		print "Stats are not available. Generating now..."
		for op in range(0,10):
			initsq = None
			check = 0
			while initsq == None and check < 10:
				initsq = getInitSquares(i,j,k,True)
				check += 1
			if initsq != [] and initsq != None:
				r1 = runAlgorithm(i,k,'dfs',initsq,True)
				if r1[3] > 10:
					r2 = copy.deepcopy(r1)
					r2[-2] = 2**r2[3]
					r2[-1] = 'N/A'
				else:
					r2 = runAlgorithm(i,k,'ids',initsq,True)
				A1.append([initsq,r1])
				A2.append([initsq,r2])
		f1 = open(str(i)+"_"+str(j)+"_"+str(k)+"_dfs_analysis.pkl","wb")
		f2 = open(str(i)+"_"+str(j)+"_"+str(k)+"_ids_analysis.pkl","wb")
		pickle.dump(A1,f1)
		pickle.dump(A2,f2)
		f1.close()
		f2.close()
	if ret:
		return (A1,A2)


def analysis():
	for j in range(0,110,10):
		for k in range(1,4):
			for i in range(2,6):
				runRandom(j,k,i)

def graph(pct,fsq,size):
	print "Fetching Stats..."
	t = runRandom(pct,fsq,size,True)
	print "Stats fetched."
	A1,A2 = t
	a1 = 0
	count1=0
	for a in A1:
		if len(a)==2:
			b = len(a[1][2])
			a1 += b
			count1+=1
	a1 /= count1
	a2 = 0
	count2=0
	for a in A2:
		if len(a)==2:
			b = len(a[1][2])
			a2 += b
			count2+=1
	a2 /= count2
	return (a1,a2)

if __name__=="__main__":
	analysis()
	# print runRandom(30,2,4,True)