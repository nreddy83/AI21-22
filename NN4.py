import sys; args = sys.argv[1:]
myLines = open(args[0],"r").read().splitlines()
#Neha Reddy, Pd4, 2024
import math
old_weights = [line.split() for line in myLines]
init_weights = []
for weightlst in old_weights:
    if "#" in weightlst: continue
    lst = []
    for w in weightlst:
        nw = w + ""
        if "," in w: 
            nw = w.replace(",", "")
        lst.append(nw)
    init_weights.append(lst)
line = args[1]
print(line)

def f1(x, y, output): return x*x + y*y < output
def f2(x, y, output): return x*x + y*y <= output
def f3(x, y, output): return x*x + y*y > output
def f4(x, y, output): return x*x + y*y >= output

if "<=" in line:
    ineq = "<="
    func = f2
elif "<" in line: 
    ineq = "<"
    func = f1
if ">=" in line:
    ineq = ">="
    func = f4
elif ">" in line:
    ineq = ">"
    func = f3

radiusSquared = float(line[line.find(ineq) + len(ineq):])
radius = radiusSquared**0.5

def t3(x):
    return 1/(1+(math.e**-x))

def derivative(x): 
    return x*(1-x)

init_layer_counts = [2]
for i, lst in enumerate(init_weights):
    init_layer_counts.append(len(lst)//init_layer_counts[i])

layer_counts = [3]
for i in range(1,len(init_layer_counts)-1):
    layer_counts.append(2*init_layer_counts[i])
layer_counts.append(1)
layer_counts.append(1)

weight_counts = []
for i in range(len(layer_counts)-1):
    weight_counts.append(layer_counts[i]*layer_counts[i+1])

weights = []
lst = []
for i in range(0, len(init_weights[0]), 2):
    lst.append(str(float(init_weights[0][i])/1))
    lst.append(str(0/1))
    lst.append(str(float(init_weights[0][i+1])/1))
for i in range(0, len(init_weights[0]), 2):
    lst.append(str(0/1))
    lst.append(str(float(init_weights[0][i])/1))
    lst.append(str(float(init_weights[0][i+1])/1))
weights.append(lst)

for i in range(1, len(init_weights)-1):
    weightlst = init_weights[i]
    lst = []
    for j in range(0, len(weightlst), init_layer_counts[i]):
        for k in range(j, j+init_layer_counts[i]):
            lst.append(str(float(weightlst[k])))
        for k in range(j, j+init_layer_counts[i]):
            lst.append(str(0/1))
    for j in range(0, len(weightlst), init_layer_counts[i]):
        for k in range(j, j+init_layer_counts[i]):
            lst.append(str(0/1))
        for k in range(j, j+init_layer_counts[i]):
            lst.append(str(float(weightlst[k])))
    weights.append(lst)

lst = []
for i in range(len(init_weights[-1])):
    if func == f3 or func == f4: # if func is > or >=
        lst.append(str(float(init_weights[-1][i])/(radius**2)))
        lst.append(str(float(init_weights[-1][i])/(radius**2)))
        v = (1+math.e)/(2*math.e)
    else: 
        lst.append(str(-float(init_weights[-1][i])/(radius**2)))
        lst.append(str(-float(init_weights[-1][i])/(radius**2)))
        v = 1.85914
weights.append(lst)
weights.append([str(v)])

def printLayerCount(lst):
    s = ""
    for l in lst:
        s += str(l) + " "
    return s

print("Layer counts:", printLayerCount(layer_counts))
for i, weight in enumerate(weights):
    s = ""
    for w in weight:
        s += w + " "
    print(s)
#Neha Reddy, Pd4, 2024