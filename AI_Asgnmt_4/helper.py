#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

def oddseq(num):
	cx,cy = 0,num/2
	seq = []
	sq = []
	while len(sq) < num*num:
		idx = cx*num + cy
		if idx not in sq:
			sq.append(idx)
			cx,cy = (cx - 1 + num)%num, (cy + 1 + num)%num 
		else:
			cx,cy = (cx + 1 + num)%num, (cy - 1 + num)%num 
			cx = (cx + 1 + num)%num
	return sq

def deseq(num):
	seq = {}
	for i in range(num):
		for j in range(num):
			seq[num*i+j] = num*i+j+1
			
	for i in range(0,num/4):
		for j in range(0,num/4):
			seq[num*i+j] = num*num - num*i-j
			
	for i in range(0,num/4):
		for j in range(3*num/4,num):
			seq[num*i+j] = num*num - num*i-j
			
	for i in range(3*num/4,num):
		for j in range(0,num/4):
			seq[num*i+j] = num*num - num*i-j
			
	for i in range(3*num/4,num):
		for j in range(3*num/4,num):
			seq[num*i+j] = num*num - num*i-j
			
	for i in range(num/4,3*num/4):
		for j in range(num/4,3*num/4):
			seq[num*i+j] = num*num - num*i-j
	
	sq = {}
	
	for i in range(num):
		for j in range(num):
			sq[seq[i*num+j]] = i*num+j
			
	return sq.values()
	
def oddSeqToSolTransformer(num):
	sq = oddseq(num)
	data = {}
	for i,s in enumerate(sq):
		data[s] = i+1
	sq = data.values()
	chunks = [sq[x:x+num] for x in xrange(0, len(sq), num)]
	return chunks,num

def seseq(num):
	if num % 2 == 1:
		num += 1
	while num % 4 == 0:
		num += 2
 
	u = [[0 for j in range(num)] for i in range(num)]
	w = num // 2
	oddSq = oddSeqToSolTransformer(w)
 
	for i in range(0, w):
		for j in range(0, w):
			u[i][j] = oddSq[0][i][j]
			u[i + w][j + w] = oddSq[0][i][j] + w*w
			u[i + w][j] = oddSq[0][i][j] + 2*w*w
			u[i][j + w] = oddSq[0][i][j] + 3*w*w
 
	l = w/2
	for i in range(0, w):
		for j in range(0, num):
			if j < l or j > num - l or (i == l and j == l):
				if not (j == 0 and i == l):
					t = u[j][i]
					u[j][i] = u[j][i + w]
					u[j][i + w] = t
	for i in range(0, num):
		for j in range(0, num):
			d[u[0][i][j]] = i*num+j
	return d.values()
	
def getSequence(num):
	if num%2 == 1:
		return oddseq(num)
	elif num%4 == 0:
		return deseq(num)
	elif (num-2)%4 == 0:
		return seseq(num)
	
if __name__ == '__main__':
	deseq(4)