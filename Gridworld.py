import sys; args = sys.argv[1:]
import math

area = int(args[0])
width = 0
height = 0
ctr = 1

if len(args) > 1:
    nums = "1234567890"
    if args[1][0] in nums: 
        width = int(args[1])
        ctr = 2
        height = area//width

def dimensions(area):
    for i in range(math.floor(area**0.5), area):
        if area%i == 0: return i, area//i
    return area, 1

if width == 0: width, height = dimensions(area)

nbrs = {}
def makeNbrs(area):
    dct = {}
    for i in range(area):
        lst = []
        if i - width >= 0: lst.append(i - width)
        if i%width > 0: 
            if i-1 not in lst: lst.append(i - 1)
        if i%width < width-1: lst.append(i + 1)
        if i+width < area: 
            if i + width not in lst: lst.append(i + width)
        dct[i] = lst
    return dct

nbrs = makeNbrs(area)
currentNbrs = makeNbrs(area)

policies = ["."]*area
rewards = [0]*area
way = ""

defaults = args[ctr:]

for func in defaults:
    default = 12
    if "G" in func.upper():
        if "0" in func: way = "G0"
        else: way = "G1"
    elif "R" in func.upper():
        if ":" in func: 
            if func[1] == ":": default = int(func[2:])
            else:
                ind = int(func[1:func.find(":")])
                policies[ind] = "*"
                rewards[ind] = int(func[func.find(":")+1:])
        else:
            ind = int(func[1:])
            policies[ind] = "*"
            rewards[ind] = default
    else:
        if func[-1] not in nums: 
            ind = int(func[1:-1])
            direction = func[-1] 
            if direction == "N": val = ind - width
            if direction == "S": val = ind + width
            if direction == "W": val = ind - 1
            if direction == "E": val = ind + 1
            if val >= area or val < 0: continue
            if val in currentNbrs[ind]: 
                currentNbrs[ind].remove(val)
                currentNbrs[val].remove(ind)
            else: 
                currentNbrs[ind].append(val)
                currentNbrs[val].append(ind)
        else:
            ind = int(func[1:])
            lst = []
            for nbr in nbrs[ind]:
                if nbr in currentNbrs[ind]: 
                    currentNbrs[nbr].remove(ind)
                else: 
                    lst.append(nbr)
                    currentNbrs[nbr].append(ind)
            currentNbrs[ind] = lst

if way == "": way = "G1"

def maxReward(rewards):
    dct = {}
    for i, val in enumerate(rewards):
        if val == 0: continue
        if val in dct: dct[val].append(i)
        else: dct[val] = [i]
    lst = []
    for val in dct:
        lst.append((val, dct[val]))
    lst.sort(reverse = True)
    fin = []
    for v1, v2 in lst:
        fin.append(v2)
    return fin

def g0(currentNbrs, rewards, policies):
    maxRewards = maxReward(rewards)
    for ind in range(len(policies)):
        if policies[ind] == "*": continue
        bestInds, bestLen = g0shortestPath(ind, currentNbrs, maxRewards, rewards, 0)
        polst = ""
        for nbr in currentNbrs[ind]:
            b = g0recur(nbr, currentNbrs, bestInds, rewards)
            if len(b) > bestLen: continue
            if len(b) == 0: continue
            direction = findDirection(ind, nbr)
            if direction not in polst: polst += direction
        finalPol = ""
        if "U" in polst: finalPol += "U"
        if "D" in polst: finalPol += "D"
        if "L" in polst: finalPol += "L"
        if "R" in polst: finalPol += "R"
        policies[ind] = findPolicy(finalPol)
    return policies

def g0recur(start, currentNbrs, maxRewards, rewards):
    if start in maxRewards: return [start]
    if rewards[start] != 0 and start not in maxRewards: return []
    parseMe = [start] 
    dctSeen = {start: None} 
    ctr = 0
    while parseMe:
        node = parseMe[0] 
        for nbr in currentNbrs[node]:
            if rewards[nbr] != 0 and nbr not in maxRewards: continue
            if nbr not in dctSeen: 
                if nbr in maxRewards: 
                    moves = [start, nbr]
                    while node != start:
                        moves.insert(1, node)
                        node = dctSeen[node]
                    return moves
                parseMe.append(nbr)
                dctSeen[nbr] = node
        parseMe.remove(node)
        ctr += 1
    return []

def g0shortestPath(start, currentNbrs, maxReward, rewards, idx):
    while idx < len(maxReward):
        maxRewards = maxReward[idx]
        parseMe = [start] 
        dctSeen = {start: None} 
        moves = []
        while parseMe:
            node = parseMe[0] 
            for nbr in currentNbrs[node]:
                if nbr not in dctSeen:
                    if rewards[nbr] != 0 and nbr not in maxRewards: continue
                    if nbr in maxRewards: 
                        moves = [start, nbr]
                        while node != start:
                            moves.insert(1, node)
                            node = dctSeen[node]
                        return maxRewards, len(moves) - 1
                    parseMe.append(nbr)
                    dctSeen[nbr] = node
            parseMe.remove(node)
        idx += 1
    return [], -1

def g1(currentNbrs, rewards, policies):
    maxRewards = maxReward(rewards)
    for ind in range(len(policies)):
        if policies[ind] == "*": continue
        bestInds, bestLen = g1shortestPathHelper(ind, currentNbrs, maxRewards, 0)
        polst = ""
        for nbr in currentNbrs[ind]:
            b = g1recur(nbr, currentNbrs, bestInds, rewards)
            if len(b) > bestLen: continue
            if len(b) == 0: continue
            direction = findDirection(ind, nbr)
            if direction not in polst: polst += direction
        finalPol = ""
        if "U" in polst: finalPol += "U"
        if "D" in polst: finalPol += "D"
        if "L" in polst: finalPol += "L"
        if "R" in polst: finalPol += "R"
        policies[ind] = findPolicy(finalPol)
    return policies

def g1recur(start, currentNbrs, maxRewards, rewards):
    if start in maxRewards: return [start]
    if rewards[start] != 0 and start not in maxRewards: return []
    parseMe = [start] 
    dctSeen = {start: None} 
    ctr = 0
    while parseMe:
        node = parseMe[0] 
        for nbr in currentNbrs[node]:
            if rewards[nbr] != 0 and nbr not in maxRewards: continue
            if nbr not in dctSeen: 
                if nbr in maxRewards: 
                    moves = [start, nbr]
                    while node != start:
                        moves.insert(1, node)
                        node = dctSeen[node]
                    return moves
                parseMe.append(nbr)
                dctSeen[nbr] = node
        parseMe.remove(node)
        ctr += 1
    return []

def g1shortestPath(start, currentNbrs, maxReward, idx):
    maxRewards = maxReward[idx]
    parseMe = [start] 
    dctSeen = {start: None} 
    moves = []
    while parseMe:
        node = parseMe[0] 
        for nbr in currentNbrs[node]:
            if nbr not in dctSeen:
                if nbr in maxRewards: 
                    moves = [start, nbr]
                    while node != start:
                        moves.insert(1, node)
                        node = dctSeen[node]
                    return maxRewards, len(moves) - 1
                parseMe.append(nbr)
                dctSeen[nbr] = node
        parseMe.remove(node)
    return [], -1

def g1shortestPathHelper(start, currentNbrs, maxReward, idx):
    storeRewards = []
    while idx < len(maxReward):
        v1, v2 = g1shortestPath(start, currentNbrs, maxReward, idx)
        storeRewards.append((v1, v2))
        idx += 1
    mx = 0
    mxLen = -1
    mxRw = []
    for v1, v2 in storeRewards:
        val = len(v1)/v2
        if val > mx:
            mx = val
            mxLen = v2
            mxRw = v1
    return mxRw, mxLen

def findDirection(idx1, idx2):
    if idx2 - idx1 == 1: return "R"
    if idx2 - idx1 == width: return "D"
    if idx1 - idx2 == 1: return "L"
    if idx1 - idx2 == width: return "U"

def findPolicy(st):
    if st in "UDLR" and len(st) == 1: return st
    if st == "UDLR": return "+"
    if st == "UD": return "|"
    if st == "LR": return "-"
    if st == "UR": return "V"
    if st == "DL": return "E"
    if st == "UL": return "M"
    if st == "DR": return "S"
    if st == "UDR": return "W"
    if st == "UDL": return "F"
    if st == "ULR": return "N"
    if st == "DLR": return "T"
    return "."

if max(rewards) == 0: policies = ["."]*area
elif way == "G0": policies = g0(currentNbrs, rewards, policies)
else: policies = g1(currentNbrs, rewards, policies)

s = ""
for p in policies:
    s += p
print(s)
#Neha Reddy, Pd.4, 2024