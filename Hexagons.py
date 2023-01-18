import sys; args = sys.argv[1:]


sets = [{0, 1, 2, 6 ,7, 8}, {2,3,4,8,9,10}, {5, 6, 7, 12, 13, 14},
          {9, 10, 11, 16, 17, 18}, {13, 14, 15,  19, 20, 21}, {15, 16, 17, 21, 22, 23},{7, 8, 9, 14, 15, 16},
          {0, 1, 2, 3, 4}, {5, 6, 7, 8, 9, 10, 11}, { 12, 13, 14, 15, 16, 17, 18}, {19, 20, 21, 22, 23},
          {5, 12, 13, 19, 20}, {0, 6, 7, 14, 15, 21, 22}, {1, 2, 8, 9, 16, 17, 23}, {3, 4, 10, 11, 18}, {1,0,6,5,12}, 
          {3,2,8,7,14,13,19}, {4,10,9,16,15,21,20},{11,18,17,23,22}]
list = [ set({}) for i in range(24)]
for i in range(24):
    for con in sets:
        if i not in con: continue
        for j in con:
            if j != i:
                list[i].add(j)
                
puzzle = "."*24
def isFinished(puzzle):
    for ind, i in enumerate(puzzle):
        if i=='.': return ind
    return -1  
symbols = {*"1234567"}
def isInvalid(pzl, index1):
    
    sub = list[index1]
    main = pzl[index1]
    
    for ind in sub:
        if pzl[ind] == main:  
                       
            return True
    return False   
def finalCheck(puzzle):
    for ind, i in enumerate(puzzle):
        for j in sets[ind]:
            if i==puzzle[j]: return False

    return True

def solve(puzzle):
    
    index = isFinished(puzzle)
    if  not (index + 1): 
         return puzzle  
    print(index)    
    
    for val in symbols:        
        pzl = puzzle[:index]+val+puzzle[index+1:] 
        
        
        if isInvalid(pzl, index): continue    
        sol = solve(pzl)
        if sol: return sol 
    return ""
print(solve(puzzle))


#for con in sets: