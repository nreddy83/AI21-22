import sys; args = sys.argv[1:]
import math
banditsTotal = {}
banditsLen = {}

def argmax(banditsTot, banditsLen):
    mx = 0
    mxb = 0
    for i in banditsTot:
        avg = banditsTot[i]/banditsLen[i]
        if avg > mx: 
            mx = avg
            mxb = i
    return mx, mxb

def bandit(testNum, armIdx, pullVal):
    global banditsTotal
    global banditsLen
    if testNum == 0: 
        banditsTotal = {i: 0 for i in range(armIdx)}
        banditsLen = {i: 0 for i in range(armIdx)}
    else: 
        banditsTotal[armIdx] += pullVal
        banditsLen[armIdx] += 1
    if testNum < 10: return testNum%10
    else: 
        lst = []
        for i in range(10): 
            lst.append(banditsTotal[i]/banditsLen[i] + 0.85*(1.00000000001**testNum)*((math.log(testNum)/banditsLen[i])**0.5))
        mx = max(lst)
        return lst.index(mx)
#Neha Reddy, Pd.4, 2024