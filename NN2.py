import sys; args = sys.argv[1:]
myLines = open(args[0],'r').read().splitlines()
import math
import random

networks = []
for line in myLines:
    inputs = line[:line.find("=>")-1].split()
    inputs.append(1)
    outputs = line[line.find("=>") + 2:].split()
    networks.append((inputs, outputs))

def t3(x):
    return 1/(1+(math.e**-x))

def feedfwd(inputs, weights):
    nC = len(weights[-1])
    cellcts = [nC]
    for w in weights[::-1][1:]:
        cn = int(len(w))/nC
        cellcts.append(int(cn))
        nC = cn
    cells = [[0 for i in range(cell)] for cell in cellcts]
    cells.reverse()
    cells[0] = inputs
    cell = 0
    ct = 0
    if len(cells) > 1:
        for w in weights[0]:
            if ct % len(cells[0]) == 0 and ct != 0:
                cell += 1
                ct = 0
            val = float(cells[0][ct])*float(w)
            #print(cells)
            cells[1][cell] += val
            ct += 1
        for layer in range(1, len(cells)-1):
            cell = 0
            ct = 0
            for w in weights[layer]:
                if ct % len(cells[layer]) == 0 and ct != 0:
                    cell += 1
                    ct = 0
                val = t3(float(cells[layer][ct]))*float(w)
                #print(cells)
                cells[layer+1][cell] += val
                ct += 1
    output = cells[-1]
    outputs = []
    if len(cells) == 1:
        for idx,cl in enumerate(output):
            outputs.append(float(cl)*float(weights[-1][idx]))
    else:
        for idx,cl in enumerate(output):
            calc = t3(float(cl))*float(weights[-1][idx])
            outputs.append(calc)
    #outputString = str(outputs)[1:-1]
    #print(outputString)
    cells.append(outputs)
    return cells

def derivative(x):
    return t3(x)*(1-t3(x))

def dotprod(lst1, lst2):
    lst = hadamard(lst1, lst2)
    sum = 0
    for i in lst:
        sum += i
    return sum

def hadamard(lst1, lst2):
    h = []
    for i in range(len(lst1)):
        if i < len(lst2): h.append(float(lst1[i])*float(lst2[i]))
        else: continue
    return h

def backprop1(network, weights, i):
    inp, output = networks[i]
    output_err = 0
    for j in range(len(output)):
        output_err += (float(output[j]) - float(network[-1][j]))*(float(output[j]) - float(network[-1][j]))
    if output_err <= 0.01: return network, weights, output_err
    errors = [[0 for j in range(len(network[j]))] for i in range(4)]
    for i in range(len(network[3])):
        errors[3][i] = float(output[i]) - network[3][i]
    for i in range(len(network[2])):
        errors[2][i] = (float(output[i])-network[-1][i])*weights[-1][i]*derivative(float(network[len(network)-2][i]))
    for i in range(len(network[1])):
        #print(errors[2])
        #print(weights[1][i: len(weights[1]): len(network[1])])
        errors[1][i] = (dotprod(errors[2], weights[1][i: len(weights[1]): len(network[1])]))*derivative(float(network[1][i]))
    for i in range(len(network[0])):
        #errors[0][i] = network[0][i]
        errors[0][i] = 0
    #print(errors)
    #errors[len(network)-4][i] = (dotprod(errors[len(network)-3], weights[0][i: len(weights[0]): len(network)-3]))*derivative(float(network[len(network)-4][i]))
    grad = [[0 for j in range(len(weights[i]))] for i in range(3)]
    for i in range(len(network[1])):
        for j in range(len(network[0])):
            grad[0][i*len(network[0])+j] = float(network[0][j])*errors[1][i]*0.1
    for i in range(len(network[2])):
        for j in range(len(network[1])):
            grad[1][i*len(network[1])+j] = float(network[1][j])*errors[2][i]*0.1
    for i in range(len(network[3])):
        grad[2][i] = float(network[2][i])*errors[3][i]*0.1
    for i in range(len(network[1])):
        for j in range(len(network[0])):
            weights[0][i*len(network[0])+j] += grad[0][i*len(network[0])+j]
    for i in range(len(network[2])):
        for j in range(len(network[1])):
            weights[1][i*len(network[1])+j] += grad[1][i*len(network[1])+j]
    for i in range(len(network[3])):
        for j in range(len(network[2])):
            weights[2][i*len(network[2])+j] += grad[2][i*len(network[2])+j]
    network = feedfwd(inputs, weights)
    for j in range(len(output)):
        output_err += (float(output[j]) - float(network[-1][j]))*(float(output[j]) - float(network[-1][j]))
    return network, weights, output_err

def backprop2(network, weights, i):
    inp, output = networks[i]
    output_err = 0
    for j in range(len(output)):
        output_err += (float(output[j]) - float(network[-1][j]))*(float(output[j]) - float(network[-1][j]))
    output_err = output_err/2
    if output_err <= 0.01: return network, weights, output_err
    errors = [[0 for j in range(len(network[i]))] for i in range(4)]
    for i in range(len(network[3])):
        errors[3][i] = float(output[i]) - network[3][i]
    for i in range(len(network[2])):
        errors[2][i] = (float(output[i])-network[-1][i])*weights[-1][i]*derivative(float(network[len(network)-2][i]))
    for i in range(len(network[1])):
        #print(errors[2])
        #print(weights[1][i: len(weights[1]): len(network[1])])
        errors[1][i] = (dotprod(errors[2], weights[1][i: len(weights[1]): len(network[1])]))*derivative(float(network[1][i]))
    for i in range(len(network[0])):
        #errors[0][i] = network[0][i]
        errors[0][i] = 0
    #print(errors)
    #errors[len(network)-4][i] = (dotprod(errors[len(network)-3], weights[0][i: len(weights[0]): len(network)-3]))*derivative(float(network[len(network)-4][i]))
    grad = [[0 for j in range(len(weights[i]))] for i in range(3)]
    for i in range(len(network[1])):
        for j in range(len(network[0])):
            grad[0][i*len(network[0])+j] = float(network[0][j])*errors[1][i]*0.1
    for i in range(len(network[2])):
        for j in range(len(network[1])):
            grad[1][i*len(network[1])+j] = float(network[1][j])*errors[2][i]*0.1
    for i in range(len(network[3])):
        grad[2][i] = float(network[2][i])*errors[3][i]*0.1
    for i in range(len(network[1])):
        for j in range(len(network[0])):
            weights[0][i*len(network[0])+j] += grad[0][i*len(network[0])+j]
    for i in range(len(network[2])):
        for j in range(len(network[1])):
            weights[1][i*len(network[1])+j] += grad[1][i*len(network[1])+j]
    for i in range(len(network[3])):
        weights[2][i] += grad[2][i]
    network = feedfwd(inputs, weights)
    for j in range(len(output)):
        output_err += (float(output[j]) - float(network[-1][j]))*(float(output[j]) - float(network[-1][j])) 
    return network, weights, output_err

for k, (inputs,outputs) in enumerate(networks):
    output_err = 100
    network = [inputs, [0]*2, [0]*len(outputs), [0]*len(outputs)]
    weights = []
    for i in range(len(network) - 2):
        weights.append([random.random() for j in range(len(network[i])*len(network[i+1]))])
    weights.append([random.random() for j in range(len(outputs))])
    if len(outputs) == 1:
        while output_err > 0.01:
            network = feedfwd(inputs, weights)
            net, wts, o_e = backprop1(network, weights, k)
            if o_e > output_err: continue
            for i in range(len(weights)):
                for j in range(len(weights[i])):
                    weights[i][j] = wts[i][j]
            for i in range(len(network)):
                for j in range(len(network[i])):
                    network[i][j] = net[i][j]
            printstr = "layer counts: " + str(len(inputs)) + " 2 " + str(len(outputs)) + " " + str(len(outputs)) + "\n"
            for weight in weights:
                for w in weight: 
                    printstr += str(w) + " "
                printstr += "\n"
            print(printstr)
            #print(weights)
            print(network)
            output_err = o_e
    else:
        while output_err > 0.01:
            network = feedfwd(inputs, weights)
            net, wts, o_e = backprop2(network, weights, k)
            if o_e > output_err: continue
            for i in range(len(weights)):
                for j in range(len(weights[i])):
                    weights[i][j] = wts[i][j]
            for i in range(len(network)):
                for j in range(len(network[i])):
                    network[i][j] = net[i][j]
            printstr = "layer counts: " + str(len(inputs)) + " 2 " + str(len(outputs)) + " " + str(len(outputs)) + "\n"
            for weight in weights:
                for w in weight: 
                    printstr += str(w) + " "
                printstr += "\n"
            print(printstr)
            #print(weights)
            #print(network)
            output_err = o_e
#Neha Reddy, Pd4, 2024