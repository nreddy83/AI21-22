import sys; args = sys.argv[1:]
# Neha Reddy, Pd 4

import time
import math
begin = time.time()
#length = int(math.sqrt(len(args[0])))
length = 3

def solvable(start, goal):
   s1 = start.replace("_", "")
   s2 = goal.replace("_", "")
   ic1 = 0
   ic2 = 0
   
   for i in range(len(s1)):
      for j in range(i+1, len(s1)):
         if s1[i] > s1[j]: ic1 += 1
         if s2[i] > s2[j]: ic2 += 1
            
   if length % 2 == 0 and ((ic1 + (start.find("_")//length))%2) == ((ic2 + (goal.find("_")//length))%2): return True
   if length % 2 == 1 and ic1 % 2 == ic2 % 2: return True
   return False

def BFS(start, goal):
   if solvable(start, goal) == False: return banded_print([start], "-1")
   if start == goal: return banded_print([start], "0")
   parseMe = [start] 
   dctSeen = {start:None} 
   moves = []
   
   while parseMe:
      node = parseMe[0] 
      for nbr in neighbors(node):
         if nbr not in dctSeen: 
            if nbr == goal: 
               moves = [start, goal]
               while node != start:
                  moves.insert(1, node)
                  node = dctSeen[node]
               return banded_print(moves, str(len(moves)-1))
            parseMe.append(nbr)
            dctSeen.update({nbr:node})
      parseMe.remove(node)
    
def neighbors(puzzle):
   ret = []
   x = puzzle.find("_")
   if x < length-gWidth: #checks if x is in the bottom row, if not swaps with bottom value
       ret.append(swap(puzzle, x+gWidth, x))
   if x >= gWidth: #checks if x is in the top row, if not swaps with top value
       ret.append(swap(puzzle, x-gWidth, x))
   if x % gWidth != 0: #checks if x is in the left column, if not swaps with left value
       ret.append(swap(puzzle, x-1, x))
   if (x+1) % gWidth != 0: #checks if x is in the right column, if not swaps with right value
       ret.append(swap(puzzle, x+1, x))
   return ret

def swap(puzzle, displaced, displacer): #helper function of neighbors
   if displacer < displaced:
       displaced, displacer = displacer, displaced
   return puzzle[:displaced] + puzzle[displacer] + puzzle[displaced + 1:displacer] + puzzle[displaced] + puzzle[displacer + 1:]
   
    
def make_neighbor(puzzle, index):
   if index > 0: return (puzzle[:puzzle.find("_") - index] + "_" + puzzle[puzzle.find("_") - index+1:puzzle.find("_")] + puzzle[puzzle.find("_") - index] + puzzle[puzzle.find("_") + 1:])
   return (puzzle[:puzzle.find("_")] + puzzle[puzzle.find("_") - index] + puzzle[puzzle.find("_") + 1:puzzle.find("_") - index] + "_" + puzzle[puzzle.find("_") - index + 1:])
        
def banded_print(moves, steps):
   width = height = length
   line = ""
   for ct in range(len(moves)//5):
      for row in range(height):
         line += moves[5*ct + 0][row*width:(row+1)*width] + "  " + moves[5*ct + 1][row*width:(row+1)*width] + "  " + moves[5*ct + 2][row*width:(row+1)*width] + "  " + moves[5*ct + 3][row*width:(row+1)*width] + "  " + moves[5*ct + 4][row*width:(row+1)*width] + "  "
         print(line)
         line = ""
   
   for row in range(height):
      if 5*(len(moves)//5) < len(moves): line += moves[5*(len(moves)//5)][row*width:(row+1)*width] + "  "
      if 5*(len(moves)//5) + 1 < len(moves): line += moves[5*(len(moves)//5) + 1][row*width:(row+1)*width] + "  "
      if 5*(len(moves)//5) + 2 < len(moves): line += moves[5*(len(moves)//5) + 2][row*width:(row+1)*width] + "  "         
      if 5*(len(moves)//5) + 3 < len(moves): line += moves[5*(len(moves)//5) + 3][row*width:(row+1)*width] + "  "
      if 5*(len(moves)//5) + 4 < len(moves): line += moves[5*(len(moves)//5) + 4][row*width:(row+1)*width] + "  "
      print(line)
      line = ""
  
   print("Steps: " + steps)
   total = abs(begin - time.time())
   print("Time: " + format(total,".3f") + "s") if total < 1 else print("Time: " + format(total,".2f") + "s")

root= "1_2345678"
length = len(root)
gHeight = int(math.sqrt(length))
while length % gHeight != 0:
  gHeight -= 1
gWidth = length//gHeight
#global look-up tables
goalIndices={x:(root.index(x)//gWidth,root.index(x)%gWidth) for x in root if x!='_'}


def manhattan(pzl):
  running_sum=0
  for idx, x in enumerate(pzl):
      if x!='_':
       running_sum+=abs((idx//gWidth)-goalIndices[x][0])+abs((idx%gWidth)-goalIndices[x][1])
  return running_sum


def BFSCounts(start):
   seenItems = {start} #node to parent

   buckets = [[] for i in range(0,32)]
   buckets[0] = [start]
   buckets1 = [[] for i in range(0,32)]
   buckets1[0] = [start]
   pointer = 0
   while pointer < 32: 
      if not buckets1[pointer]:
         pointer+=1
         continue
   
      current = buckets1[pointer].pop(0)
      for nbr in neighbors(current):
         if nbr not in seenItems:
            buckets[pointer+1].append(nbr)
            buckets1[pointer+1].append(nbr)
            seenItems.add(nbr)
   y = 0
   for element in buckets:
      print(y, len(element))
      y+=1
   return buckets

def BFSNbrCounts(start):
   parseMe = [start] 
   dctSeen = {start:None} 
   nbrcounts = [[] for i in range(4)]
   dctLevel = {start:0}
   
   while parseMe:
      node = parseMe[0] 
      nbrs = neighbors(node)
      g = dctLevel[node]
      for nbr in nbrs:
         if nbr not in dctSeen: 
            parseMe.append(nbr)
            dctSeen[nbr] = node
            dctLevel[nbr] = g + 1
      parseMe.remove(node)
   
   for elem in dctSeen:
      b = True
      nbrs = neighbors(elem)
      for nbr in nbrs:
         if dctLevel[elem] < dctLevel[nbr]: b = False
      if b: nbrcounts[len(nbrs) - 1].append(elem)
   y = 1
   for element in nbrcounts:
      print(y, len(element))
      y+=1
      
   
# start = args[0]
# goal = "12345678_"
# if len(args) > 1: goal = args[1]
# BFS(start, goal)
BFSNbrCounts("1_2345678")