import sys; args = sys.argv[1:]
import math

myLines = []
for i, arg in enumerate(args): myLines.append(arg)

width = 0
height = 0
str = ""

if len(myLines) == 1: 
    str = myLines[0]
    l = len(str)
    for i in range(1, int(math.sqrt(l))+1):
        if l%i == 0: 
            height = i
            width = l//i
else: 
    str = myLines[0]
    width = int(myLines[1])
    height = len(str)//int(width)

rowIdx = [[*range(rs,rs+width)] for rs in range(0,len(str),width)]
colIdx = [[*range(cs,len(str),width)] for cs in range(width)]

revRowIdx = []
revColIdx = []
for x in rowIdx:
   temp = []
   for y in reversed(x):
      temp.append(y)
   revRowIdx.append(temp)
for x in colIdx:
   temp = []
   for y in reversed(x):
      temp.append(y)
   revColIdx.append(temp)

def rev(str):
   newStr = ''
   for x in reversed(range(len(str))): 
      newStr += str[x]
   return newStr

def lstStr(lst,str):
    newStr = ''
    for x in lst: 
       for i in x: newStr += str[i]
    return newStr

def rotationlst(str, height, width):
    one = str
    two = lstStr(revRowIdx,str)
    three = lstStr(colIdx,str)
    four = lstStr(revColIdx,str)
    rots = [one]
    if two not in rots: rots.append(two)
    if three not in rots: rots.append(three)
    if four not in rots: rots.append(four) 
    r2 = rev(two)
    r1 = rev(one)
    r3 = rev(three)
    r4 = rev(four)
    if r1 not in rots: rots.append(r1)
    if r2 not in rots: rots.append(r2)
    if r3 not in rots: rots.append(r3)
    if r4 not in rots: rots.append(r4)     
    return rots

lst = rotationlst(str, height, width)
for l in lst:
    print(l)

#Neha Reddy, pd. 4, 2024