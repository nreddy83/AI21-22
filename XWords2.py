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
if block%2 == 1: puzzle = OPENCHAR*mid + BLOCKCHAR + OPENCHAR*mid
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
            if ch != BLOCKCHAR:
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
            if ch != BLOCKCHAR:
                constraints.append(stc)
                constraints.append(area-stc-1)
            stc += 1
        puzzle = ""
        for ch in pzl:
            puzzle += ch
        return puzzle

seedstr = seedStr(puzzle, fixed).upper()

def placeBlocks(puzzle, ltrCount): # recursively places blocks on the puzzle until all constraints are met and total number of blocks is met
    if puzzle.count(BLOCKCHAR) > block: return "No solution"
    if puzzle.count(BLOCKCHAR) == block: 
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
        if i in constraints or puzzle[i] == BLOCKCHAR: continue
        if puzzle[i] == OPENCHAR: 
            pzl = [*puzzle]
            pl = ""
            pzl[i] = BLOCKCHAR
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
            f = fill(pl, connected(pl), 0)
            if f.count(BLOCKCHAR) <= block: pl = f
            else: pl = fill(pl, connected(pl), 1)
            bF = placeBlocks(pl, ltrCount)
            if bF != "No solution": return bF
    return "No solution"

def placeBlocks(puzzle, ltrCount): # recursively places blocks on the puzzle until all constraints are met and total number of blocks is met
    if puzzle.count(BLOCKCHAR) > block: return "No solution"
    if puzzle.count(BLOCKCHAR) == block: 
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
        if i in constraints or puzzle[i] == BLOCKCHAR: continue
        if puzzle[i] == OPENCHAR: 
            pzl = [*puzzle]
            pl = ""
            pzl[i] = BLOCKCHAR
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
            f = fill(pl, connected(pl), 0)
            if f.count(BLOCKCHAR) <= block: pl = f
            else: pl = fill(pl, connected(pl), 1)
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
                pzl[rowPositions[i][j+1]] = BLOCKCHAR
                pzl[rowPositions[i][j+2]] = BLOCKCHAR
            if row[j: j+3] == s2:
                pzl[rowPositions[i][j+1]] = BLOCKCHAR
        if row[0:3] == s3: 
            pzl[rowPositions[i][0]] = BLOCKCHAR
            pzl[rowPositions[i][1]] = BLOCKCHAR
        if row[0:2] == s4:
            pzl[rowPositions[i][0]] = BLOCKCHAR
        if row[len(row) - 3: len(row)] == s5:
            pzl[rowPositions[i][len(row)-2]] = BLOCKCHAR
            pzl[rowPositions[i][len(row)-1]] = BLOCKCHAR
        if row[len(row) - 2: len(row)] == s6:
            pzl[rowPositions[i][len(row)-1]] = BLOCKCHAR
    for i,cols in enumerate(colPositions):
        col = ""
        for idx in cols:
            col += puzzle[idx]
        for j in range(len(col) - 3):
            if j+3 < len(col) and col[j:j+4] == s1:
                pzl[colPositions[i][j+1]] = BLOCKCHAR
                pzl[colPositions[i][j+2]] = BLOCKCHAR
            if col[j: j+3] == s2:
                pzl[colPositions[i][j+1]] = BLOCKCHAR
        if col[0:3] == s3: 
            pzl[colPositions[i][0]] = BLOCKCHAR
            pzl[colPositions[i][1]] = BLOCKCHAR
        if col[0:2] == s4:
            pzl[colPositions[i][0]] = BLOCKCHAR
        if col[len(col) - 3: len(col)] == s5:
            pzl[colPositions[i][len(col)-2]] = BLOCKCHAR
            pzl[colPositions[i][len(col)-1]] = BLOCKCHAR
        if col[len(col) - 2: len(col)] == s6:
            pzl[colPositions[i][len(col)-1]] = BLOCKCHAR
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
    if OPENCHAR not in puzzle: return set()
    if len(constraints) > 0: start = constraints[0]
    else: start = puzzle.find(OPENCHAR)
    parseMe = [start]
    seen = {start}
    while parseMe:
        node = parseMe[0] 
        for nbr in neighbors(node):
            if puzzle[nbr] == BLOCKCHAR: continue
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
            pzl[i] = BLOCKCHAR
    puzzle = ""
    for ch in pzl:
        puzzle += ch
    return puzzle

def checkMatch(word1, word2):
    if len(word1) != len(word2): return False
    for i in range(len(word2)):
        if word2[i] != OPENCHAR and word2[i] != word1[i]: return False
    return True

def possibles(s, dct):
    st = set()
    if s == OPENCHAR*len(s): return {*dct[len(s)]}
    for word in dct[len(s)]:
        if checkMatch(word, s) == True: st.add(word)
    return st

def initializeDct(puzzle, dctWords):
    dct = {}
    i = 0
    s = ""
    r1 = 0
    r2 = 0
    # horizontal
    row = 1
    #if w >= h: 
    bool = i%h < w
    #else: bool = i%w < h
    while i < area and bool:
        if puzzle[i] == BLOCKCHAR or i == row*h-1:
            if puzzle[i] != BLOCKCHAR: s += puzzle[i]
            if i == row*h-1: row += 1
            if r2 != 0: dct["h"+str(r1)] = possibles(s, dctWords)
            s = ""
            r1 = 0
            r2 = 0
            lsth = []
        else: 
            if s == "": r1 = i
            s += puzzle[i]
            r2 += 1
        i+=1
    i = 0
    s = ""
    v1 = 0
    v2 = 0
    # vertical
    col = 0
    while col < h and i < area and i%h == col:
        if puzzle[i] == BLOCKCHAR or i//h == w-1:
            if puzzle[i] != BLOCKCHAR: s += puzzle[i]
            if i//h == w-1:
                col += 1
                i = col
            else:
                i += h
            if v2 != 0: dct["v"+str(v1)] = possibles(s, dctWords)
            s = ""
            v1 = 0
            v2 = 0
        else:
            if s == "": v1 = i
            s += puzzle[i]
            v2 += h
            i += h
    return dct
    
def optimalplace(dct):
    least = 99999
    leastrange = ""
    if len(dct) == 0: return leastrange
    for rang in dct:
        if len(dct[rang]) < least:
            least = len(dct[rang])
            leastrange = rang
    return leastrange

def placeWords(puzzle, seedstr, dctRange):
    #print(displayPuzzle(puzzle))
    #print()
    if dctRange == {}: dctRange = initializeDct(puzzle, myWords)
    if OPENCHAR not in puzzle: #puzzle is filled in
        for i, ch in enumerate(seedstr): #checking that the seedstrings match up
            if seedstr[i] != OPENCHAR:
                if seedstr[i] != puzzle[i]: return "No solution"
        dct = initializeDct(puzzle, myWords)
        for ranges in dct:
            if len(dct[ranges]) == 0: return "No solution"
        return puzzle
    if len(dctRange) == 0: return "No solution"
    rang = optimalplace(dctRange)
    if len(rang) == 0: return "No solution"
    direc = rang[0]
    ind = int(rang[1:])
    dctRanges = {}
    for word in dctRange[rang]:
        if direc == "h": 
            pzl = placeHorizontally(puzzle, word, ind)
            for ranges in dctRange:
                if ranges == rang: continue
                dctRanges[ranges] = set()
                if ranges[0] == "h": 
                    for wd in dctRange[ranges]:
                        if wd == word: continue
                        dctRanges[ranges].add(wd)
                else:
                    s = ""
                    startidx = int(ranges[1:])
                    while startidx < area and pzl[startidx] != BLOCKCHAR:
                        s += pzl[startidx]
                        startidx += h
                    for wd in dctRange[ranges]:
                        if wd == word: continue
                        if checkMatch(wd, s) == False: continue 
                        dctRanges[ranges].add(wd)
            board = ""
            for ch in pzl:
                board += ch
            pW = placeWords(board, seedstr, dctRanges)
            if pW != "No solution": return pW
        else: 
            pzl = placeVertically(puzzle, word, ind)
            for ranges in dctRange:
                if ranges == rang: continue
                dctRanges[ranges] = set()
                if ranges[0] == "v": 
                    for wd in dctRange[ranges]:
                        if wd == word: continue
                        dctRanges[ranges].add(wd)
                else:
                    s = ""
                    startidx = int(ranges[1:])
                    startpos = startidx
                    while startidx < ((startpos//h)+1)*h and pzl[startidx] != BLOCKCHAR:
                        s += pzl[startidx]
                        startidx += 1
                    for wd in dctRange[ranges]:
                        if wd == word: continue
                        if checkMatch(wd, s) == False: continue
                        dctRanges[ranges].add(wd)
            board = ""
            for ch in pzl:
                board += ch
            pW = placeWords(board, seedstr, dctRanges)
            if pW != "No solution": return pW
    return "No solution"

def placeWords2(puzzle, seedstr): # incrementally places words until the whole puzzle is filled - baseline rough draft version
    pzl = [*puzzle]
    tempDct = {}
    for i in myWords:
        tempDct[i] = myWords[i]
    start = -1
    for pzlpos, ch in enumerate(puzzle):
        if ch != BLOCKCHAR: 
            start = pzlpos
            break
    scol = start%h
    i = 0
    while i < len(colPositions[0]):
        col = colPositions[scol][i]
        col1 = col
        s = ""
        l = 0
        if puzzle[col] != BLOCKCHAR:
            while i < len(colPositions[0]) and puzzle[col] != BLOCKCHAR:
                s += puzzle[col]
                col += h
                i += 1
                l += 1
            wrd = tempDct[l]
            s = s.replace(OPENCHAR, "\w")
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
            if puzzle[ridx] != BLOCKCHAR:
                rst = ridx
                l = 0
                s = ""
                savei = i
                while i < len(row) and puzzle[ridx] != BLOCKCHAR:
                    s += puzzle[ridx]
                    l += 1
                    ridx += 1
                    i += 1
                wrd = tempDct[l]
                s = s.replace(OPENCHAR, "\w")
                wd = re.search(s, str(tempDct[l]))
                if wd: wrd = wd.group()
                if wd == None: 
                    ridx = rst
                    l = 0
                    s = ""
                    i = savei
                    while i < len(row) and cpypuzzle[ridx] != BLOCKCHAR:
                        s += cpypuzzle[ridx]
                        l += 1
                        ridx += 1
                        i += 1
                    wrd = tempDct[l]
                    s = s.replace(OPENCHAR, "\w")
                wd = re.search(s, str(tempDct[l]))
                if wd: wrd = wd.group()
                elif OPENCHAR and "\w" not in s: wrd = s
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
    for i, ch in enumerate(pzl):
        if seedstr[i] != OPENCHAR and pzl[i] != seedstr[i]: pzl[i] = seedstr[i]
    for ch in pzl:
        puzzle += ch
    return puzzle

def placeHorizontally(pzl, word, start):
    puzzle = [*pzl]
    for i in range(len(word)):
        puzzle[start+i] = word[i]
    return puzzle

def placeVertically(pzl, word, start):
    puzzle = [*pzl]
    for i in range(len(word)):
        puzzle[start+i*h] = word[i]
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
    if t.count(BLOCKCHAR) <= block: puzzle = t
    else: puzzle = fill(puzzle, connected(puzzle), 1)
    puzzle = placeBlocks(puzzle, ltrCount)
    print(displayPuzzle(puzzle))
    print()
    alt = placeWords2(puzzle, seedstr)
    print(displayPuzzle(alt))
    print()
    puzzle = placeWords(puzzle, seedstr, {})
    if puzzle != "No solution": print(displayPuzzle(puzzle))

structure(puzzle)
print(abs(time.process_time() - beginning))
# Neha Reddy, Pd. 4, 2024