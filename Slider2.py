import sys; args = sys.argv[1:]
myPuzzles = open(args[0], "r").read().splitlines()
import time
import math
begin = time.process_time()
length = 3
# length = int(math.sqrt(len(myPuzzles[0])))
final = myPuzzles[0]
dctInd = {}
for ind, ch in enumerate(final):
    dctInd.update({ch: ind})

#determines if it's possible to get from one puzzle to another
def solvable(start, goal):
   s1 = start.replace("_", "")
   s2 = goal.replace("_", "")
   ic1 = 0
   ic2 = 0

   for i in range(15):
      for j in range(i+1, 15):
         if s1[i] > s1[j]: ic1 += 1
         if s2[i] > s2[j]: ic2 += 1

   if (ic1 + (start.find("_")//4))%2 == (ic2 + (goal.find("_")//4))%2: return True
   #if length % 2 == 1 and ic1 % 2 == ic2 % 2: return True
   return False

#calculates the optimal way to get from a starting slider puzzle to the goal
def AStar(root, goal):
   #f = new estimate, g = level, h = manhattan distance, openSet = list, closedSet = dct
   if root == goal: return ("G", "0")
   openSet = [[] for i in range(30)]
   ptr = pos = 0
   openSet[ptr].append((root, root)) #paren, child
   closedSet = {} #paren:child
   while openSet:
      while len(openSet[ptr]) == pos:
        pos = 0
        ptr += 1
      puzzle, child = openSet[ptr][pos] #retrieving puzzle with smallest f
      pos += 1
      if puzzle in closedSet: continue #no need to add it again if it's already in dct
      closedSet[puzzle] = child #optimal add and not already in it
      for nbr, ch in neighbors(puzzle):
         if nbr == goal:
            closedSet[goal] = puzzle
            return find_path(closedSet)
         if nbr in closedSet: continue #no need to add it back if it's already in dct
         openSet[ptr + small_h(puzzle, nbr, ch)].append((nbr, puzzle)) #(new node, new child)

#finds the h value but only recalculating one char
def small_h(puzzle1, puzzle2, ch):
    p1 = puzzle1.find(ch)
    p2 = puzzle2.find(ch)
    go = dctInd[ch]
    dist1 = abs(p1//4 - go//4) + abs(p1%4 - go%4)
    dist2 = abs(p2//4 - go//4) + abs(p2%4 - go%4)
    return dist2 > dist1

#helper for the neighbors function - switches the positions of space and where it moves to
def swap(pzl, p1, p2):
    pzlList = [*pzl]
    ch = pzlList[p2]
    pzlList[p1],pzlList[p2] = pzlList[p2],pzlList[p1]
    return (("".join(pzlList)), ch)

#finds the neighbors of each slider puzzle
def neighbors(puzzle):
   if ind == 0: return [swap(puzzle, 0, 1), swap(puzzle, 0, 3)]
   if ind == 1: return [swap(puzzle, 1, 0), swap(puzzle, 1, 2), swap(puzzle, 1, 4)]
   if ind == 2: return [swap(puzzle, 2, 1), swap(puzzle, 2, 3), swap(puzzle, 2, 5)]
   if ind == 3: return [swap(puzzle, 3, 4), swap(puzzle, 3, 6)]
   if ind == 4: return [swap(puzzle, 4, 1), swap(puzzle, 4, 3), swap(puzzle, 4, 5), swap(puzzle, 4, 7)]
   if ind == 5: return [swap(puzzle, 5, 2), swap(puzzle, 5, 4), swap(puzzle, 5, 8)]
   if ind == 6: return [swap(puzzle, 6, 3), swap(puzzle, 6, 7)]
   if ind == 7: return [swap(puzzle, 7, 4), swap(puzzle, 7, 6), swap(puzzle, 7, 8)]
   if ind == 8: return [swap(puzzle, 8, 5), swap(puzzle, 8, 7)]


#calculates direction to get from puzzle1 to puzzle2
def find_direction(puzzle1, puzzle2):
   if puzzle1.find("_") - puzzle2.find("_") == 4: return "U"
   if puzzle2.find("_") - puzzle1.find("_") == 4: return "D"
   if puzzle1.find("_") - puzzle2.find("_") == 1: return "L"
   if puzzle2.find("_") - puzzle1.find("_") == 1: return "R"
   else: return ""

#takes in the dictionary from AStar and retrieves the path
def find_path(dct):
   path = ""
   node = final
   steps = 0
   while node != dct[node]: #{root:root}
      path += find_direction(dct[node], node)
      steps += 1
      node = dct[node]
   return (path[::-1], str(steps)) #reversed because path is calculated backwards

#goes through every puzzle in the file and prints the puzzle, time it was solved in and the letter path of it
for puzzle in myPuzzles:
   path, steps = AStar(puzzle, final) #gets letter path and number of steps
   print(steps + ": " + puzzle + " solved in " + format(abs(time.process_time()-begin),".1f") + " secs with a path length of " + steps + " => path " + path)

# Neha Reddy, Pd 4, 2024