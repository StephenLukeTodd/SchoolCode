###STEPHEN LUKE TODD
###ADVANCED DATA STRUCTURES
import time
def computeSpans1(P):
    S = []
    start = time.time()
    for i in range(len(P)):
        k = 0
        done = False
        while (k<=i) and not done:
                if (P[i-k] <= P[i]):
                    k = k+1
                else:
                    done = True
        S.append(k)
    end = time.time()
    return S, end
P=[4,3,1,2,1,3,7]
S=computeSpans1(P)
print(S)

