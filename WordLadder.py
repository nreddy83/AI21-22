import sys; args = sys.argv[1:]
myWords = open(args[0], "r").read().splitlines()
myWords = set(myWords)
#Neha Reddy, Pd 4, 2024
import time
begin = time.process_time()

nodes = {}
letters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}
length = len(myWords)
print("Word count: " + str(length))

def neighbors(word):
   neighbors = set()
   for ind in range(6):
      for letter in letters:
         temp = str([word[:ind] + letter + word[ind+1:]])[2:-2]
         if temp in myWords and temp not in neighbors:
            neighbors.add(temp)
   return neighbors
   
for word in myWords:
   adj = []
   nbrs = neighbors(word)
   for nbr in nbrs:
      if nbr in myWords and not nbr == word:
         adj += [nbr]
   nodes.update({word: adj})
total = abs(time.process_time() - begin)

val_lengths = []
count = 0
for elem in nodes:
   val = len(nodes.get(elem))
   val_lengths += [val]
   count += val
   
print("Edge count: " + str(count//2))

degrees = ""
for i in range (max(val_lengths) + 1):
   degrees += str(val_lengths.count(i)) + " "
   
print("Degree List: " + degrees)
print("Construction time: " + format(total,".3f") + "s") if total < 1 else print("Construction time: " + format(total,".2f") + "s") if total < 10 else print("Construction time: " + format(total,".1f") + "s")

def conn_comp_size(word):
   parseMe = [word] 
   dctSeen = {word:None}
   length = 1
   
   while parseMe:
      node = parseMe[0] 
      for nbr in nodes.get(node):
         if nbr not in dctSeen: 
            length += 1
            parseMe += [nbr]
            dctSeen.update({nbr:node})
      parseMe.remove(node)
   return length

if len(args) > 1:
   word1 = str(args[1])
   word2 = str(args[2])
   
   second = ""
   component_sizes = []
   
   for word in myWords:
      if len(nodes.get(word)) + 1 == max(val_lengths): second = word
      size = conn_comp_size(word)
      if size not in component_sizes: component_sizes += [size]
   print("Second degree word: " + second)
   
   k2 = 0
   k3 = 0
   k4 = 0
   largest = 0
   for node in nodes:
      current = nodes.get(node)
      if len(current) > 0: current0 = current[0]
      if len(current) > 1: current1 = current[1]
      if len(current) > 2: current2 = current[2]
      if len(current) == 1 and len(nodes.get(current0)) == 1: k2 += 1
      if len(current) == 2 and len(nodes.get(current0)) == 2 and current1 in nodes.get(current0) and len(nodes.get(current1)) == 2 and current0 in nodes.get(current1): k3 += 1
      if len(current) == 3 and len(nodes.get(current0)) == 3 and current1 in nodes.get(current0) and current2 in nodes.get(current0) and len(nodes.get(current1)) == 3 and current0 in nodes.get(current1) and current2 in nodes.get(current1) and len(nodes.get(current[2])) == 3 and current0 in nodes.get(current2) and current1 in nodes.get(current2): k4 += 1
   
   parseMe = [word1] 
   dctSeen = {word1:None}
   path = []
   farthest = ""
   length = 0
   current = 0
   
   while parseMe:
      node = parseMe[0] 
      for nbr in nodes.get(node):
         if nbr not in dctSeen: 
            current += 1
            if length < current:
               length = current
               farthest = nbr
            if nbr == word2: 
               path = [word1, word2]
               temp = node
               while temp != word1:
                  path.insert(1, temp)
                  temp = dctSeen[temp]
            parseMe += [nbr]
            dctSeen.update({nbr:node})
      parseMe.remove(node)
   
   adj = []
   nbrs = neighbors(word1)
   for nbr in nbrs:
      if nbr in myWords and not nbr == word1:
         adj += [nbr]
   nodes.update({word1: adj})
      
   adj = []
   nbrs = neighbors(word2)
   for nbr in nbrs:
      if nbr in myWords and not nbr == word2:
         adj += [nbr]
   nodes.update({word2: adj})
     
   print("Connected component size count: " + str(len(component_sizes)))
   print("Largest component size: " + str(max(component_sizes)))
   print("K2 count: " + str(k2//2))
   print("K3 count: " + str(k3//3))
   print("K4 count: " + str(k4//4))
   print("Neighbors: " + str(nodes.get(word1)))
   print("Farthest: " + farthest)
   print("Path: " + str(path))
#Neha Reddy, Pd 4, 2024