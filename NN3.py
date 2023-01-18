import sys; args = sys.argv[1:]
line = args[0]
import math
import random
import time
start = time.process_time()
num_cases = 12000
alpha = 0.5

def f1(x, y, output): return x*x + y*y < output
def f2(x, y, output): return x*x + y*y <= output
def f3(x, y, output): return x*x + y*y > output
def f4(x, y, output): return x*x + y*y >= output

def t3(x): return 1/(1+(math.e**-x))

def derivative(x): return x*(1-x)

#read in inputs
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

radius = float(line[line.find(ineq) + len(ineq):])

#create NN of random weights
layer_counts = [3, 4, 4, 3, 1, 1] #[3, 4, 6, 3, 4, 1, 1]
weight_counts = [12, 16, 12, 1, 1] #[12, 24, 18, 12, 1, 1]
weights = [[[random.uniform(-1, 1) for i in (range(layer_counts[id]))] for j in range(layer_counts[id+1])] for id, k in enumerate(weight_counts)]
cells = [[0 for j in range(lc)] for lc in layer_counts]
actual = [[0] for i in range(num_cases)]
expected = [[1] for i in range(num_cases)]

training_cases = []

for i in range(num_cases):
    x = random.uniform(-1.5, 1.5)
    y = random.uniform(-1.5, 1.5)
    output = int(func(x, y, radius))
    training_cases.append(([x, y], [output]))

def feedfwd(inputs, weights):
    network = []
    return network

total_err = 10000000000000000000000000

def printWL(layer):
    lst = []
    for x in layer:
        for weigh in x:
            lst.append(weigh)
    return lst

def hadamard(errors, weights):
    hdmd = [elem*weights[idx] for idx,elem in enumerate(errors)]
    return hdmd

def valid(actual, expected):
    e = 0
    for index, a in enumerate(actual):
        e += err(a, expected[index])
    return e

def err(output, expected):
    lst = [(expected[i] - output[i])**2 for i in range(len(expected))]
    return sum(lst)/2
    
def update_weights(gradient, weights):
    myLines = [[*lst] for lst in weights]
    for i, layer in enumerate(weights):
        for idx, w in enumerate(layer):
            for id, weight in enumerate(w):
                myLines[i][idx][id] = weight + (gradient[i][idx][id]*alpha)
    return myLines

def getGradient(cells, errors, weights):
    gradient = [[[0 for i in j] for j in k] for k in weights]
    for ind, k in enumerate(gradient): #each layer
        for id,j in enumerate(k): #each cell (next layer's cells)
            for idx, i in enumerate(j): #each weight (previous layer's cells)
                gradient[ind][id][idx] = cells[ind][idx]*errors[ind][id%len(errors[ind])]
    return gradient

def getFrom(layer, j):
    return [layer[n][j] for n in range(len(layer))]

def getErrors(cells, weights, outputs):
    errors = [[0 for cell in k] for k in cells[1:]]
    errors[-1] = outputs
    for i in range(len(errors)):
        if i == 0: continue
        for j in range(len(errors[-i-1])):
            errors[-i-1][j] = sum(hadamard(errors[-i], getFrom(weights[-i],j)))*derivative(cells[len(cells)-i-1][j])
    return errors

def feedfwd(cells, weights):
    cs = [[cell for cell in c] for c in cells]
    for idx in range(len(cs)-1):
        for ind in range(len(cs[idx+1])):
            if idx != len(cs)-2:
                cs[idx+1][ind] = t3(sum(hadamard(cs[idx],weights[idx][ind])))
            else: 
                cs[idx+1][ind] = sum(hadamard(cs[idx],weights[idx][ind]))
    return cs

def findnetworks():
    networks = []
    for i in range(num_cases):
            inputs, outputs = training_cases[i]
            for index,o in enumerate(outputs):
                outputs[index] = float(o)
            for index,input in enumerate(inputs):
                inputs[index] = float(input)
            inputs.append(1)
            cells[0] = [*inputs]
            cs = [[*cells[k]] for k in range(len(cells))]
            networks.append((cs, outputs))
    return networks

network = findnetworks()
e_curr = valid(actual, expected)
while e_curr > 0.01:
    for i in range(num_cases):
        net = network[i][0]
        outputs = network[i][1]
        net = feedfwd(net, weights)
        outputE = [t-net[-1][l] for l,t in enumerate(outputs)]
        errors = getErrors(net, weights, outputE)
        gradient = getGradient(net, errors, weights)
        weights = update_weights(gradient, weights)
        actual[i] = net[-1]
        expected[i] = outputs
    if e_curr < total_err:
        print()
        print("layer counts:", str(layer_counts)[1:-1])
        for w in weights:
            print(str(printWL(w))[1:-1]) 
        total_err = e_curr
        print("err", total_err)
        if total_err < 55: alpha = .00008*math.sqrt(total_err)
        elif total_err < 65: alpha = .0003*math.sqrt(total_err)
        elif total_err < 75: alpha = .0005*math.sqrt(total_err)
        elif total_err < 85: alpha = .0008*math.sqrt(total_err)
        elif total_err < 100: alpha = .003*math.sqrt(total_err)
        elif total_err < 150: alpha = .005*math.sqrt(total_err)
        elif total_err < 500: alpha = .01*math.sqrt(total_err)
    e_curr = valid(actual, expected)
print()
print("layer counts:", str(layer_counts)[1:-1])
for w in weights:
    print(str(printWL(w))[1:-1])
print("time")
print(abs(time.process_time()-start))
#Neha Reddy, Pd.4, 2024