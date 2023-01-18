import sys; args = sys.argv[1:]
myPuzzles = open(args[0], "r").read().splitlines()
# Neha Reddy, Pd 4, 2024
import math
import time
#len_total = len(myPuzzles[0])
len_total = 81
#plength = int(math.sqrt(len_total)) #lookup for the side length of each puzzle
plength = 9
chars = [*"123456789"]
#1 dct way storing tuples: 8-20s for all 128 puzzles on laptop
#find the symbol with the fewest possible positions per constraint set (in as many pblites list as possible!!) - improves number of choices

# def dimensions(): #lookup for height and width of each subpuzzle
#     for i in range(int(math.sqrt(plength)), len_total):
#         if len_total%i == 0: return i, plength//i

# spheight, spwidth = dimensions()

def checkSum(puzzle): #should always be 324
    sum = 0
    min = 9999
    for ch in puzzle:
        val = ord(ch)
        sum += val
        if val < min: min = val
    return sum - len_total*min

#prints 2D array can be used for debugging purposes
def printPuzzle(puzzle, ind):
    display = "" 
    for row in range(plength):
        for col in range(plength):
            if row == 0: display += puzzle[row*plength + col] + " "
            else: display += puzzle[row*plength + col] + " "
        if row != plength-1: display += "\n"
        if row != plength-1: display += " "*(len(str(ind)) + 2)
    return display

#lookup tables to check each group for duplicates - makes a list of lists of each group's indices
positions = [{*range(col, len_total, plength)} for col in range(plength)]
rowPositions = [{*range(row*plength, (row+1)*plength)} for row in range(plength)]
subblockPositions = [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {6, 7, 8, 15, 16, 17, 24, 25, 26},
{27, 28, 29, 36, 37, 38, 45, 46, 47}, {30, 31, 32, 39, 40, 41, 48, 49, 50}, {33, 34, 35, 42, 43, 44, 51, 52, 53},
{54, 55, 56, 63, 64, 65, 72, 73, 74}, {57, 58, 59, 66, 67, 68, 75, 76, 77}, {60, 61, 62, 69, 70, 71, 78, 79, 80}]
#subblockPositions = [{((brow + row*spheight)*plength) + ((bcol + col*spwidth)*plength) for brow in range(spheight) for bcol in range(spwidth)} for row in range(spheight) for col in range(spwidth)]
positions.extend(rowPositions)
positions.extend(subblockPositions)

#lookup table for each index's column, row, and subblock groups (list of indexes)
dctPositions = {i: {ind for ind, group in enumerate(positions) if i in group} for i in range(len_total)}

#lookup table for each index's neighbors (indicies in the same group as it)
dctNeighbors = {i: {ind for group in dctPositions[i] for ind in positions[group]} for i in range(len_total)}

def possibilities(puzzle, i):
    lst = {chars[j] for j in range(plength)}
    for pos in dctNeighbors[i]:
        if puzzle[pos] not in lst: continue
        lst.remove(puzzle[pos])
    return frozenset(lst)

#recalculates the number of possibilities for each dot
def optimal_dot(puzzle):
    toReturn = {}
    for i in range(len_total):
        if puzzle[i] != ".": continue
        final = possibilities(puzzle, i)
        if len(final) not in toReturn: toReturn[len(final)] = {(final, i)}
        else: toReturn[len(final)].add((final, i))
    return toReturn

def isInvalid(puzzle, idx, dct):
    if idx == -1: return False
    if 0 in dct and len(dct[0]) > 0: return True #one index has no possibilities
    for i in dctPositions[idx]:
        c = ""
        for ind in positions[i]:
            if puzzle[ind] != ".": c += puzzle[ind]
            if c.count(puzzle[ind]) > 1: return True
    return False

def bruteForce(puzzle, idx, dctPossibilities):
    if isInvalid(puzzle, idx, dctPossibilities): return ""
    if puzzle.count(".") == 0: return puzzle
    if idx == -1: dctPossibilities = optimal_dot(puzzle)
    pb = set()
    i = -1
    for ind in range(plength+1):
        if pb != set() and i != -1: break
        if ind in dctPossibilities: 
            for tpblites, ti in dctPossibilities[ind]:
                if puzzle[ti] == ".": 
                    pb = tpblites
                    i = ti
                    break
    for ch in pb:
        pzl = puzzle[:i] + ch + puzzle[i+1:]
        newdctP = {}
        if pzl.count(".") == 1: bF = bruteForce(pzl, i, dctPossibilities)
        else: 
            for l in dctPossibilities:
                for pblites, ind in dctPossibilities[l]:
                    if ind == i: continue
                    if ind in dctNeighbors[i]: pblites = pblites - {ch}
                    if len(pblites) not in newdctP: newdctP[len(pblites)] = {(pblites, ind)}
                    else: newdctP[len(pblites)].add((pblites, ind))
            bF = bruteForce(pzl, i, newdctP)
        if bF: return bF #puzzle is solved
    return "" #puzzle is unsolvable

begin = time.process_time()
for ind, puzzle in enumerate(myPuzzles):
    print(str(ind + 1) + ": ", end = "")
    print(puzzle)
    solved = bruteForce(puzzle, -1, {})
    print(" "*(len(str(ind + 1)) + 2), end = "") #lines up starting puzzle to solved puzzle
    print(solved, end = " ")
    print("check sum:", checkSum(solved), end = " ")
    print("time:", str(abs(time.process_time() - begin)))
# Neha Reddy, Pd 4, 2024