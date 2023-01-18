import sys; args = sys.argv[1:]
#solves 11/12 blocks puzzles - speedup: only place blocks at edges
chars = "abcdefghijklmnopqrstuvwxyz"
bigBlockArea = 0 # counts up the area of the big block to compare to smaller rectangles for impossible case
ptr = 1
if "x" in args[0].lower(): 
    curr = args[0].lower()
    p1 = int(curr[:curr.find("x")])
    p2 = int(curr[curr.find("x")+1:])
else:
    p1 = int(args[0])
    p2 = int(args[1])        
    ptr += 1
bigBlock = [p2, p1] # stores the big block as a list of 2 dimensions 
bigBlockArea = p1*p2
puzzle = [["." for i in range(p2)] for j in range(p1)]

smallBlocks = [] # stores the smaller rectangles as a list of list of 2 dimensions
totArea = 0 # counts up the total area of the smaller blocks to compare to big block for impossible case
while ptr < len(args):
    if "x" in args[ptr].lower(): 
        curr = args[ptr].lower()
        p1 = int(curr[:curr.find("x")])
        p2 = int(curr[curr.find("x")+1:])
    else:
        p1 = int(args[ptr])
        p2 = int(args[ptr+1])
        ptr += 1
    a = p1*p2
    smallBlocks.append((a, [p1, p2]))
    totArea += a
    ptr += 1

def placeable(puzzle, x1, y1, x2, y2):
    for i in range(x1, x2):
        for j in range(y1, y2):
            if puzzle[i][j] != ".": return False
    return True

def placeBlock(puzzle, block, pos):
    lst = []
    ch = chars[pos]
    if pos == 0:
        #orientation 1
        if block[0] <= bigBlock[0] and block[1] <= bigBlock[1]: #in bounds
            cpy = [["." for i in range(bigBlock[0])] for j in range(bigBlock[1])]
            for b in range(block[0]):
                for a in range(block[1]):
                    cpy[a][b] = ch
            lst.append(cpy)
        #orientation 2
        if block[1] <= bigBlock[0] and block[0] <= bigBlock[1]: #in bounds
            cpy = [["." for i in range(bigBlock[0])] for j in range(bigBlock[1])]
            for b in range(block[1]):
                for a in range(block[0]):
                    cpy[a][b] = ch
            lst.append(cpy)
        return lst
    #orientation 1
    for i in range(bigBlock[0] - block[0] + 1):
        for j in range(bigBlock[1] - block[1] + 1):
            if placeable(puzzle, j, i, j + block[1], i + block[0]):
                cpy = []
                for cpyi in puzzle:
                    temp = []
                    for cpyj in cpyi:
                        temp.append(cpyj)
                    cpy.append(temp)
                for b in range(i, block[0]+i):
                    for a in range(j, block[1]+j):
                        cpy[a][b] = ch
                if cpy not in lst: lst.append(cpy)
    #orientation 2
    if block[0] == block[1]: return lst # if not a square - no need to try rotation positions if it looks the same once rotated
    for i in range(bigBlock[0] - block[1] + 1):
        for j in range(bigBlock[1] - block[0] + 1):
            if placeable(puzzle, j, i, j + block[0], i + block[1]):
                cpy = []
                for cpyi in puzzle:
                    temp = []
                    for cpyj in cpyi:
                        temp.append(cpyj)
                    cpy.append(temp)
                for b in range(i, block[1]+i):
                    for a in range(j, block[0]+j):
                        cpy[a][b] = ch
                if cpy not in lst: lst.append(cpy)
    return lst

def decompPrint(puzzle):
    decomp = "Decomposition: "
    used = []
    for h, lst in enumerate(puzzle):
        w = 0
        while w < len(lst):
            ch = lst[w]
            if ch == ".":
                decomp += "1x"+str(lst.count(".")) + " "
                w += lst.count(".")
            if ch != "." and ch not in used:
                used.append(ch)
                pos = chars.find(ch)
                ar, b = smallBlocks[pos]
                ct = ar//lst.count(ch)
                decomp += str(ct)+"x"+str(lst.count(ch)) + " "
            w += 1
    return decomp

def bruteForce(puzzle, pos):
    if pos >= len(smallBlocks): return decompPrint(puzzle)
    ar, block = smallBlocks[pos]
    places = placeBlock(puzzle, block, pos)
    idx = 0
    while idx < len(places):
        place = places[idx]
        cpy = []
        for lst in place: 
            temp = []
            for char in lst:
                temp.append(char)
            cpy.append(temp)
        bF = bruteForce(cpy, pos+1)
        if bF != "No solution": return bF
        idx += 1
    return "No solution" # no solution case

if totArea > bigBlockArea: print("No solution") # one case of no solution
else: 
    smallBlocks.sort(reverse=True)
    print(bruteForce(puzzle, 0))
# Neha Reddy, Pd4, 2024