import sys; args = sys.argv[1:]
myLines = open(args[0],'r').read().splitlines()
import math
weights = [line.split() for line in myLines]

def t1(x):
    return x
def t2(x):
    return x if x > 0 else 0
def t3(x):
    return 1/(1+(math.e**-x))
def t4(x):
    return (2*t3(x)) - 1

inputs = args[2:]
nC = len(weights[-1])
cellcts = [nC]
for w in weights[::-1][1:]:
    cn = int(len(w))/nC
    cellcts.append(int(cn))
    nC = cn
cells = [[0 for i in range(cell)] for cell in cellcts]
cells.reverse()
cells[0] = inputs

if args[1] == "T1": func = t1
if args[1] == "T2": func = t2
if args[1] == "T3": func = t3
if args[1] == "T4": func = t4

cell = 0
ct = 0
if len(cells) > 1:
    for w in weights[0]:
        if ct % len(cells[0]) == 0 and ct != 0:
            cell += 1
            ct = 0
        val = float(cells[0][ct])*float(w)
        print(cells)
        cells[1][cell] += val
        ct += 1
    
    for layer in range(1, len(cells)-1):
        cell = 0
        ct = 0
        for w in weights[layer]:
            if ct % len(cells[layer]) == 0 and ct != 0:
                cell += 1
                ct = 0
            val = func(float(cells[layer][ct]))*float(w)
            print(cells)
            cells[layer+1][cell] += val
            ct += 1

print("weights", weights)
output = cells[-1]
output1 = []
if len(cells) == 1:
    for idx,cl in enumerate(output):
        output1.append(float(cl)*float(weights[-1][idx]))
else:
    for idx,cl in enumerate(output):
        output1.append(func(float(cl))*float(weights[-1][idx]))
outputString = str(output1)[1:-1]
print(outputString)
#Neha Reddy, Pd4, 2024