###STEPHEN LUKE TODD
###ADVANCED DATA STRUCTURES
from Stack2 import*
import time
def computeSpans2(P):
    S=[]
    D= Stack()
    
    start = time.time()
    for i in range(len(P)):
        h = 0
        done = False
        while not (D.is_empty() or done):
            if P[i] >= P[D.peek()]:
                D.pop()
            else:
                done = True
        if D.is_empty():
            h = -1
        else:
            h = D.peek()

        S.append(i-h)
        D.push(i)
    end = time.time()
    return S, end

prices=[4,3,1,2,1,3,7]
print(computeSpans2(prices)) 
