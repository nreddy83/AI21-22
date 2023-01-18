import sys; args = sys.argv[1:]
dct = open(args[0], "r")
import re, time
beginning = time.process_time()
# initializing args + globals
BLOCKCHAR = "#"
OPENCHAR = "-"
myWords = {}
for word in dct:
    w = ""
    for ch in word:
        c = ch.upper()
        if c not in "QAZXSWEDCVFRTGBNHYUJMKIOLP": continue
        else: w += c
    if len(w) < 3: continue
    if len(w) in myWords: myWords[len(w)].append(w)
    else: myWords[len(w)] = [w]
dim = args[1].lower()
w = int(dim[:dim.find("x")]) # width
h = int(dim[dim.find("x")+1:]) # height
area = h*w
mid = area//2
block = int(args[2]) # number of blocking squares
ctr = 3
# dim = args[0].lower()
# w = int(dim[:dim.find("x")]) # width
# h = int(dim[dim.find("x")+1:]) # height
# area = h*w
# mid = area//2
# block = int(args[1]) # number of blocking squares
# ctr = 2
fixed = [] # list of seedstrings
while len(args) > ctr:
    fixed.append(args[ctr])
    ctr += 1
if block%2 == 1: puzzle = OPENCHAR*mid + "#" + OPENCHAR*mid
else: puzzle = OPENCHAR*area
if block == area and len(fixed) == 0: puzzle = BLOCKCHAR*area
constraints = []
colPositions = [[*range(col, area, h)] for col in range(h)]
rowPositions = [[*range(row*h, (row+1)*h)] for row in range(w)]
ltrCount = 0

def displayPuzzle(puzzle): # prints a 2d representation of the puzzle - for debugging purposes
    if puzzle == "No solution": return puzzle
    display = "" 
    for row in range(w):
        for col in range(h):
            #if (row*h+col) in constraints: display += "*" + " "
            display += puzzle[row*h + col] + " "
        if row != w-1: display += "\n"
    return display

def seedStr(puzzle, fixed): # helper method to place all the seed strings given in args
    for str in fixed: 
        str = str.upper()
        dr = str[0]
        str = str[1:]
        d1 = ""
        d2 = ""
        seed = ""
        for ch in str:
            if (ch in "QWERTYUIOPLKJHGFDSAZXCVBNM" or ch == BLOCKCHAR) and "X" in d1: 
                seed += ch
            elif "X" in d1: 
                d2 += ch
            else: d1 += ch
        if seed == "": seed = BLOCKCHAR
        d1 = int(d1[:len(d1) - 1])
        d2 = int(d2)
        puzzle = placeSeed(puzzle, d1, d2, dr.upper(), seed.upper())
    return puzzle

def placeSeed(puzzle, d1, d2, dr, word): # places the seed strings in all upper case into the puzzle with its helper method
    pzl = [*puzzle]
    stc = d1*h + d2
    if dr == "V":
        for ch in word:
            pzl[stc] = ch
            if ch != "#":
                constraints.append(stc)
                constraints.append(area-stc-1)
            stc += h
        puzzle = ""
        for ch in pzl:
            puzzle += ch
        return puzzle
    else:
        for ch in word:
            pzl[stc] = ch
            if ch != "#":
                constraints.append(stc)
                constraints.append(area-stc-1)
            stc += 1
        puzzle = ""
        for ch in pzl:
            puzzle += ch
        return puzzle

seedstr = seedStr(puzzle, fixed).upper()

def placeBlocks(puzzle, ltrCount): # recursively places blocks on the puzzle until all constraints are met and total number of blocks is met
    if puzzle.count("#") > block: return "No solution"
    if puzzle.count("#") == block: 
        ct = 0
        for row in rowPositions:
            r1 = ""
            for r in row:
                r1 += puzzle[r]
            if re.search("#[^#][^#]?#", r1) != None: return "No solution"
            if re.search("^[^#][^#]?#", r1) != None: return "No solution"
            if re.search("#[^#][^#]?$", r1) != None: return "No solution"
        for col in colPositions:
            c1 = ""
            for c in col:
                c1 += puzzle[c]
            if re.search("#[^#][^#]?#", c1) != None: return "No solution"
            if re.search("^[^#][^#]?#", c1) != None: return "No solution"
            if re.search("#[^#][^#]?$", c1) != None: return "No solution"
        for ch in puzzle:
            if ch in "QWERTYUIOPLKJHGFDSAZXCVBNM": ct += 1
        if ct != ltrCount: return "No solution"
        if len(connected(puzzle)) + block != area: return "No solution"
        return puzzle
    for i in range(len(puzzle)):
        if i in constraints or puzzle[i] == "#": continue
        if puzzle[i] == "-": 
            pzl = [*puzzle]
            pl = ""
            pzl[i] = "#"
            ct = 0
            for ch in pzl:
                pl += ch
                if ch in "QWERTYUIOPLKJHGFDSAZXCVBNM": ct += 1
            if ct != ltrCount: return "No solution"
            for row in rowPositions:
                r1 = ""
                for r in row:
                    r1 += puzzle[r]
                if re.search("#[^#][^#]?#", r1) != None: return "No solution"
                if re.search("^[^#][^#]?#", r1) != None: return "No solution"
                if re.search("#[^#][^#]?$", r1) != None: return "No solution"
            for col in colPositions:
                c1 = ""
                for c in col:
                    c1 += puzzle[c]
                if re.search("#[^#][^#]?#", c1) != None: return "No solution"
                if re.search("^[^#][^#]?#", c1) != None: return "No solution"
                if re.search("#[^#][^#]?$", c1) != None: return "No solution"
            pl = balance(pl)
            pl = reflect(pl)
            # f = fill(pl, connected(pl), 0)
            # if f.count("#") <= block: pl = f
            # else: pl = fill(pl, connected(pl), 1)
            bF = placeBlocks(pl, ltrCount)
            if bF != "No solution": return bF
    return "No solution"
    
def balance(puzzle): # removes all #--# and similar occurences
    pzl = [*puzzle]
    s1 = BLOCKCHAR + OPENCHAR*2 + BLOCKCHAR
    s2 = BLOCKCHAR + OPENCHAR + BLOCKCHAR
    s3 = OPENCHAR*2 + BLOCKCHAR        
    s4 = OPENCHAR + BLOCKCHAR
    s5 = BLOCKCHAR + OPENCHAR*2
    s6 = BLOCKCHAR + OPENCHAR
    for i, rows in enumerate(rowPositions):
        row = ""
        for idx in rows:
            row += puzzle[idx]
        for j in range(len(row) - 3):
            if j+3 < len(row) and row[j:j+4] == s1:
                pzl[rowPositions[i][j+1]] = "#"
                pzl[rowPositions[i][j+2]] = "#"
            if row[j: j+3] == s2:
                pzl[rowPositions[i][j+1]] = "#"
        if row[0:3] == s3: 
            pzl[rowPositions[i][0]] = "#"
            pzl[rowPositions[i][1]] = "#"
        if row[0:2] == s4:
            pzl[rowPositions[i][0]] = "#"
        if row[len(row) - 3: len(row)] == s5:
            pzl[rowPositions[i][len(row)-2]] = "#"
            pzl[rowPositions[i][len(row)-1]] = "#"
        if row[len(row) - 2: len(row)] == s6:
            pzl[rowPositions[i][len(row)-1]] = "#"
    for i,cols in enumerate(colPositions):
        col = ""
        for idx in cols:
            col += puzzle[idx]
        for j in range(len(col) - 3):
            if j+3 < len(col) and col[j:j+4] == s1:
                pzl[colPositions[i][j+1]] = "#"
                pzl[colPositions[i][j+2]] = "#"
            if col[j: j+3] == s2:
                pzl[colPositions[i][j+1]] = "#"
        if col[0:3] == s3: 
            pzl[colPositions[i][0]] = "#"
            pzl[colPositions[i][1]] = "#"
        if col[0:2] == s4:
            pzl[colPositions[i][0]] = "#"
        if col[len(col) - 3: len(col)] == s5:
            pzl[colPositions[i][len(col)-2]] = "#"
            pzl[colPositions[i][len(col)-1]] = "#"
        if col[len(col) - 2: len(col)] == s6:
            pzl[colPositions[i][len(col)-1]] = "#"
    puzzle = ""
    for ch in pzl:
        puzzle += ch
    return puzzle

def reflect(puzzle): # makes sure the puzzle is symmetric 180 degrees about the origin
    pzl = [*puzzle]
    for i, ch in enumerate(pzl):
        if ch == BLOCKCHAR: pzl[area-i-1] = BLOCKCHAR
    puzzle = ""
    for ch in pzl:
        puzzle += ch
    return puzzle

def neighbors(idx): # returns the indices of the neighbors (up, down, left, right) to use in determining if a puzzle is connected
    nbrs = []
    for row in rowPositions:
        for i, pos in enumerate(row):
            if idx == pos:
                if i > 0: nbrs.append(row[i-1])
                if i < len(row) - 1: nbrs.append(row[i+1])
    for col in colPositions:
        for i, pos in enumerate(col):
            if idx == pos:
                if i > 0: nbrs.append(col[i-1])
                if i < len(col) - 1: nbrs.append(col[i+1])
    return nbrs

def connected(puzzle): # uses BFS to check if every index in the puzzle is reachable if it's not a block
    if "-" not in puzzle: return set()
    if len(constraints) > 0: start = constraints[0]
    else: start = puzzle.find("-")
    parseMe = [start]
    seen = {start}
    while parseMe:
        node = parseMe[0] 
        for nbr in neighbors(node):
            if puzzle[nbr] == "#": continue
            if nbr not in seen: 
                parseMe.append(nbr)
                seen.add(nbr)
        parseMe.remove(node)
    return seen

def fill(puzzle, connects, state): # using the list from connected, fills in the non-connected regions
    if len(connects) == area: return puzzle
    pzl = [*puzzle]
    if state == 0: unseen = {*range(0, area)} - connects
    else: unseen = connects
    for i in range(len(puzzle)):
        if i in unseen: 
            if puzzle[i] in "QWERTYUIOPLKJHGFDSAZXCVBNM": return puzzle
            pzl[i] = "#"
    puzzle = ""
    for ch in pzl:
        puzzle += ch
    return puzzle

def checkMatch(word1, word2):
    if len(word1) != len(word2): return False
    for i in range(len(word2)):
        if word2[i] != "-" and word2[i] != word1[i]: return False
    return True

def possibles(puzzle, ind, dct, direc):
    if direc == "H":
        k = ind
        while k-1 >= (h*(ind//h)) and puzzle[k-1] != "#":
            k -= 1
        pos = k
        s = ""
        while pos < ((ind//h)+1)*h and puzzle[pos] != "#":
            s += puzzle[pos]
            pos += 1
        l = len(s)
    if direc == "V":
        k = ind
        while k-h >= ind%h and puzzle[k-h] != "#":
            k -= h
        pos = k
        s = ""
        while pos < area and puzzle[pos] != "#":
            s += puzzle[pos]
            pos += h
        l = len(s)
    lst = set()
    for word in dct[l]: 
        if checkMatch(word, s) == True: lst.add(word)
    return lst

def optimalstart(puzzle, dct):
    best = puzzle.find("-")
    least = 9999
    besth = set()
    bestv = set()
    for i, ch in enumerate(puzzle):
        if ch == "-":
            hp = possibles(puzzle, i, dct, "H")
            vp = possibles(puzzle, i, dct, "V")
            psblsct = len(hp) + len(vp)
            if psblsct == 0: return -1, hp, vp
            if psblsct == 2: return i, hp, vp
            if psblsct < least:
                least = psblsct
                best = i
                besth = hp
                bestv = vp
    return best, besth, bestv

def placeWords(puzzle, seedstr, myWords, used):
    if "-" not in puzzle: #puzzle is filled in
        for i, ch in enumerate(seedstr): #checking that the seedstrings match up
            if seedstr[i] != "-":
                if seedstr[i] != puzzle[i]: return "No solution"
        return puzzle
    pzl = [*puzzle]
    tempDct = {}
    for i in myWords:
        tempDct[i] = myWords[i]
    #pos = optimalstart(puzzle, dct) #start w least possibilities
    pos, setH, setV = optimalstart(puzzle, tempDct)
    if pos == -1 or len(setH) == 0 or len(setV) == 0: return "No solution"
    i = pos
    while i-1 >= (h*(pos//h)) and pzl[i-1] != "#":
        i -= 1
    j = i
    s = ""
    while j < ((i//h)+1)*h and pzl[j] != "#":
        s += pzl[j]
        j += 1
    l = len(s)
    for word in setH:
        if checkMatch(word, s): 
            if word in used or word not in tempDct[l]: continue
            if word in tempDct[l]:
                if len(tempDct[l]) > 1: tempDct[l].remove(word)
                else: tempDct[l] = myWords[l]
            pzl = placeHorizontally(pzl, word, i)
            used.append(word)
            # print("h")
            # print(displayPuzzle(pzl))
            # print()
            k = pos
            while k-h >= pos%h and pzl[k-h] != "#":
                k -= h
            n = k
            s = ""
            while k < area and pzl[k] != "#":
                s += pzl[k]
                k += h
            l = len(s)
            #setV.discard(word)
            for word2 in setV:
                if word2 in used or word2 not in tempDct[l]: continue
                if checkMatch(word2, s):
                    if word2 in tempDct[l]:
                        if len(tempDct[l]) > 1: tempDct[l].remove(word2)
                        else: tempDct[l] = myWords[l]
                    pzl = placeVertically(pzl, word2, n)
                    used.append(word2)
                    puzzle = ""
                    for ch in pzl:
                        puzzle += ch
                    # print("v")
                    # print(displayPuzzle(puzzle))
                    # print()
                    pW = placeWords(puzzle, seedstr, tempDct, used)
                    if pW != "No solution": return pW
    return "No solution"

def placeHorizontally(puzzle, word, start):
    for i in range(len(word)):
        puzzle[start+i] = word[i]
    return puzzle

def placeVertically(puzzle, word, start):
    for i in range(len(word)):
        puzzle[start+i*h] = word[i]
    return puzzle

def placeWords2(puzzle): # recursively places words until the whole puzzle is filled
    pzl = [*puzzle]
    tempDct = {}
    for i in myWords:
        tempDct[i] = myWords[i]
    start = -1
    for pzlpos, ch in enumerate(puzzle):
        if ch != "#": 
            start = pzlpos
            break
    scol = start%h
    i = 0
    while i < len(colPositions[0]):
        col = colPositions[scol][i]
        col1 = col
        s = ""
        l = 0
        if puzzle[col] != "#":
            while i < len(colPositions[0]) and puzzle[col] != "#":
                s += puzzle[col]
                col += h
                i += 1
                l += 1
            wrd = tempDct[l]
            s = s.replace("-", "\w")
            wd = re.search(s, str(tempDct[l]))
            if wd: wrd = wd.group()
            if len(tempDct[l]) > 1: 
                tempDct[l] = tempDct[l][1:]
            else:
                for mw in myWords:
                    tempDct[mw] = myWords[mw]
                for j in range(l):
                    pzl[rst+j] = wrd[j]
            for j in range(l):
                pzl[col1+h*j] = wrd[j]
            puzzle = ""
            for ch in pzl:
                puzzle += ch
        i += 1
        col += h
    cpypuzzle = ""
    for ch in puzzle: 
        cpypuzzle += ch
    for row in rowPositions:
        i = 0
        ridx = row[0]
        rst = ridx
        while i < len(row):
            if puzzle[ridx] != "#":
                rst = ridx
                l = 0
                s = ""
                savei = i
                while i < len(row) and puzzle[ridx] != "#":
                    s += puzzle[ridx]
                    l += 1
                    ridx += 1
                    i += 1
                wrd = tempDct[l]
                s = s.replace("-", "\w")
                wd = re.search(s, str(tempDct[l]))
                if wd: wrd = wd.group()
                if wd == None: 
                    ridx = rst
                    l = 0
                    s = ""
                    i = savei
                    while i < len(row) and cpypuzzle[ridx] != "#":
                        s += cpypuzzle[ridx]
                        l += 1
                        ridx += 1
                        i += 1
                    wrd = tempDct[l]
                    s = s.replace("-", "\w")
                wd = re.search(s, str(tempDct[l]))
                if wd: wrd = wd.group()
                elif "-" and "\w" not in s: wrd = s
                if len(tempDct[l]) > 1: 
                    tempDct[l] = tempDct[l][1:]
                else:
                    for mw in myWords:
                        tempDct[mw] = myWords[mw]
                for j in range(l):
                    if len(wrd[j]) == 1: 
                        pzl[rst+j] = wrd[j]
                    else: 
                        wrd = wrd[0]
                        pzl[rst+j] = wrd[j]
            i += 1
            ridx += 1
    puzzle = ""
    for ch in pzl:
        puzzle += ch
    return puzzle

def structure(puzzle):
    global ltrCount
    puzzle = seedstr
    for ch in puzzle:
        if ch in "QWERTYUIOPLKJHGFDSAZXCVBNM": ltrCount += 1
    puzzle = reflect(puzzle)
    p = balance(puzzle)
    while p != puzzle:
        puzzle = balance(puzzle)
        puzzle = reflect(puzzle)
        p = balance(puzzle)
    print(displayPuzzle(puzzle))
    print()
    t = fill(puzzle, connected(puzzle), 0)
    if t.count("#") <= block: puzzle = t
    else: puzzle = fill(puzzle, connected(puzzle), 1)
    puzzle = placeBlocks(puzzle, ltrCount)
    print(displayPuzzle(puzzle))
    print()
    if area < 50:
        alt = placeWords2(puzzle)
        print(displayPuzzle(alt))
        print()
        puzzle = placeWords(puzzle, seedstr, myWords, [])
        if puzzle != "No solution": print(displayPuzzle(puzzle))
    else:
        puzzle = placeWords2(puzzle)
        print(displayPuzzle(puzzle))

structure(puzzle)
print(abs(time.process_time() - beginning))
# Neha Reddy, Pd. 4, 2024