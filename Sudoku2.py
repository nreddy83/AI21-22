import sys; args = sys.argv[1:]
myPuzzles = open(args[0], "r").read().splitlines()
import time
len_total = 81
plength = 9 #lookup for the side length of each puzzle
chars = [*"123456789"]

#1 dct way: 25-30s for all 128 puzzles on laptop

def checkSum(puzzle): #should always be 324
    sum = 0
    min = 9999
    for ch in puzzle:
        val = ord(ch)
        sum += val
        if val < min: min = val
    return sum - len_total*min

#lookup tables to check each group for duplicates - makes a list of lists of each group's indices
positions = [{*range(col, len_total, plength)} for col in range(plength)]
rowPositions = [{*range(row*plength, (row+1)*plength)} for row in range(plength)]
subblockPositions = [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {6, 7, 8, 15, 16, 17, 24, 25, 26},
{27, 28, 29, 36, 37, 38, 45, 46, 47}, {30, 31, 32, 39, 40, 41, 48, 49, 50}, {33, 34, 35, 42, 43, 44, 51, 52, 53},
{54, 55, 56, 63, 64, 65, 72, 73, 74}, {57, 58, 59, 66, 67, 68, 75, 76, 77}, {60, 61, 62, 69, 70, 71, 78, 79, 80}]
positions.extend(rowPositions)
positions.extend(subblockPositions)

#lookup table for each index's column, row, and subblock groups (list of indexes)
dctPositions = {i: {ind for ind, group in enumerate(positions) if i in group} for i in range(len_total)}

#lookup table for each index's neighbors (indicies in the same group as it)
dctNeighbors = {i: {ind for group in dctPositions[i] for ind in positions[group]} for i in range(len_total)}

def possibilities(puzzle, i):
    lst = [chars[j] for j in range(plength)]
    for pos in dctNeighbors[i]:
        if puzzle[pos] not in lst: continue
        lst.remove(puzzle[pos])
    return lst

#recalculates the number of possibilities for each dot
def optimal_dot(puzzle):
    dct1 = {i: possibilities(puzzle, i) for i in range(len_total) if puzzle[i] == "."}
    dct2 = {ch: puzzle.count(ch) for ch in chars}
    return dct1, dct2

#returns the most optimal dot in the dictionary
def update_best(puzzle, dct):
    lst = {*"123456789"}
    idx = -1
    for key in dct:
        if puzzle[key] != ".": continue
        if len(dct[key]) < 2: return key, dct[key]
        if len(dct[key]) < len(lst):
            lst = dct[key]
            idx = key
    return idx, lst

def bruteForce(puzzle, dctPossibilities, dctSymbols):
    if len(dctPossibilities) == 0: dctPossibilities, dctSymbols = optimal_dot(puzzle)
    if puzzle.count(".") == 0: return puzzle
    pos, pblites = update_best(puzzle, dctPossibilities)
    for ch in pblites:
        nbr = puzzle[:pos] + ch + puzzle[pos+1:]
        nbrsDct = {}
        for key in dctPossibilities:
            nbrsDct[key] = list(dctPossibilities[key])
        nbrsDct.pop(pos)
        for n in dctNeighbors[pos]:
            if puzzle[n] != ".": continue 
            if n not in nbrsDct: continue 
            if ch in nbrsDct[n]: nbrsDct[n].remove(ch)
        bF = bruteForce(nbr, nbrsDct)
        if bF: return bF
    return ""

begin = time.process_time()
for ind, puzzle in enumerate(myPuzzles):
    print(str(ind + 1) + ": ", end = "")
    print(puzzle)
    solved = bruteForce(puzzle, {}, {})
    print(" "*(len(str(ind + 1)) + 2), end = "") #lines up starting puzzle to solved puzzle
    print(solved, end = " ")
    print("check sum:", checkSum(solved), end = " ")
    print("time:", str(abs(time.process_time() - begin)))

# Neha Reddy, Pd 4, 2024