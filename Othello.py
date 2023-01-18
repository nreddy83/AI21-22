import sys; args = sys.argv[1:]
chars = "ABCDEFGH"
nums = "1234567890"
board = ""
token = ""
moves = []
certain = True
moves = []
for ar in args: # initializes arguments passed in
    if len(ar) == 64: board = ar.lower()
    if ar in "xXOo": token = ar.lower()
    if len(ar) > 0 and ar[0].upper() in chars: moves.append(int(chars.find(ar[0].upper()))+((int((ar[1])) - 1)*8))
    elif len(ar) > 0 and ar[0] in nums: moves.append(int(ar))

if board == "": board = "."*27 + "ox......xo" + "."*27
if token == "": 
    certain = False
    if board.count(".") % 2 == 1: token = "o"
    else: token = "x"

def possibles(board, token, run):
    if token == "x": opp = "o"
    else: opp = "x"
    lst = []
    for i in range(len(board)):
        if board[i] == token:
            # north
            if i//8 != 0:
                pos = i - 8
                ct = 0
                while pos > 0 and board[pos] == opp:
                    pos -= 8
                    ct += 1
                if pos >= 0 and ct > 0 and board[pos] == "." and pos not in lst: lst.append(pos)
            # south
            if i//8 != 7:
                pos = i + 8
                ct = 0
                while pos < 64 and board[pos] == opp:
                    pos += 8
                    ct += 1
                if pos < 64 and ct > 0 and board[pos] == "." and pos not in lst: lst.append(pos)
            # west
            if i%8 != 0:
                pos = i - 1
                ct = 0
                while pos%8 > 0 and pos > 0 and board[pos] == opp:
                    pos -= 1
                    ct += 1
                if pos >= 0 and pos%8 >= 0 and ct > 0 and board[pos] == "." and pos not in lst: lst.append(pos)
            # east
            if i%8 != 7:
                pos = i + 1
                ct = 0
                while pos%8 < 7 and pos < 64 and board[pos] == opp:
                    pos += 1
                    ct += 1
                if pos < 64 and pos%8 <= 7 and ct > 0 and board[pos] == "." and pos not in lst: lst.append(pos)
            # northwest
            if i//8 != 0 and i%8 != 0:
                pos = i - 9
                ct = 0
                while pos%8 > 0 and pos > 0 and board[pos] == opp:
                    pos -= 9
                    ct += 1
                if pos >= 0 and pos%8 >= 0 and ct > 0 and board[pos] == "." and pos not in lst: lst.append(pos)
            # northeast
            if i//8 != 0 and i%8 != 7:
                pos = i - 7
                ct = 0
                while pos%8 < 7 and pos > 0 and board[pos] == opp:
                    pos -= 7
                    ct += 1
                if pos >= 0 and pos%8 <= 7 and ct > 0 and board[pos] == "." and pos not in lst: lst.append(pos)
            # southwest 
            if i//8 != 7 and i%8 != 7:
                pos = i + 9
                ct = 0
                while pos%8 < 7 and pos < 64 and board[pos] == opp:
                    pos += 9
                    ct += 1
                if pos < 64 and pos%8 <= 7 and ct > 0 and board[pos] == "." and pos not in lst: lst.append(pos)
            # southeast
            if i//8 != 7 and i%8 != 0:
                pos = i + 7
                ct = 0
                while pos%8 > 0 and pos < 64 and board[pos] == opp:
                    pos += 7
                    ct += 1
                if pos < 64 and pos%8 >= 0 and ct > 0 and board[pos] == "." and pos not in lst: lst.append(pos)
    if len(lst) > 0: return lst, token, opp
    if run == 0: return possibles(board, opp, 1)
    return [], opp, token

def possiblesboard(b, possibles):
    possibles.sort()
    board = ""
    itr = 0
    if len(possibles) > 0: pb = possibles[itr]
    else: pb = -1
    for i, ch in enumerate(b):
        if pb == i:
            board += "*"
            if itr+1 < len(possibles): 
                itr += 1
                pb = possibles[itr]
        else: board += ch
    return board

def makemove(board, token, opp, position):
    for i in range(len(board)):
        if i == position:
            fin = []
            #south
            if position//8 > 0 and board[position - 8] == opp:
                temp = []
                p = position - 8
                ct = 0
                while p > 0 and board[p] == opp:
                    temp.append(p)
                    p -= 8
                    ct += 1
                if ct > 0 and p >= 0 and board[p] == token: 
                    for idx in temp:
                        fin.append(idx)
            #north
            if position//8 < 7 and board[position+8] == opp:
                temp = []
                p = position + 8
                ct = 0
                while p < 64 and board[p] == opp:
                    temp.append(p)
                    p += 8
                    ct += 1
                if ct > 0 and p < 64 and board[p] == token:
                    for idx in temp:
                        fin.append(idx)
            #west
            if position - 1 > 0 and position%8 > 0 and board[position - 1] == opp:
                temp = []
                p = position - 1
                ct = 0
                while p > 0 and p%8 > 0 and board[p] == opp:
                    temp.append(p)
                    p -= 1
                    ct += 1
                if ct > 0 and p >= 0 and p%8 >= 0 and board[p] == token:
                    for idx in temp:
                        fin.append(idx)
            #east
            if position + 1 < 64 and position%8 < 7 and board[position+1] == opp:
                temp = []
                p = position + 1
                ct = 0
                while p < 64 and p%8 < 7 and board[p] == opp:
                    temp.append(p)
                    p += 1
                    ct += 1
                if ct > 0 and p < 64 and p%8 <= 7 and board[p] == token:
                    for idx in temp:
                        fin.append(idx)
            #northwest
            if position - 7 > 0 and position%8 < 7 and board[position - 7] == opp:
                temp = []
                p = position - 7
                ct = 0
                while p < 64 and p%8 < 7 and board[p] == opp:
                    temp.append(p)
                    p -= 7
                    ct += 1
                if ct > 0 and p >= 0 and p%8 <= 7 and board[p] == token:
                    for idx in temp:
                        fin.append(idx)
            #northeast
            if position - 9 > 0 and position%8 > 0 and board[position-9] == opp:
                temp = []
                p = position - 9
                ct = 0
                while p > 0 and p%8 > 0 and board[p] == opp:
                    temp.append(p)
                    p -= 9
                    ct += 1
                if ct > 0 and p >= 0 and p%8 >= 0 and board[p] == token:
                    for idx in temp:
                        fin.append(idx)
            #southwest
            if position + 9 < 64 and position%8 < 7 and board[position+9] == opp:
                temp = []
                p = position + 9
                ct = 0
                while p < 64 and p%8 < 7 and board[p] == opp:
                    temp.append(p)
                    p += 9
                    ct += 1
                if ct > 0 and p < 64 and p%8 <= 7 and board[p] == token:
                    for idx in temp:
                        fin.append(idx)
            #southeast
            if position + 7 < 64 and position%8 > 0 and board[position+7] == opp:
                temp = []
                p = position + 7
                ct = 0
                while p < 64 and p%8 > 0 and board[p] == opp:
                    temp.append(p)
                    p += 7
                    ct += 1
                if ct > 0 and p < 64 and p%8 >= 0 and board[p] == token:
                    for idx in temp:
                        fin.append(idx)
            if len(fin) > 0: 
                fin.append(i)
                return move(board, token, fin)
    return ""

def move(b, token, lst):
    if len(lst) == 0: return b
    lst.sort()
    board = ""
    ptr = 0
    idx = lst[ptr]
    for i, ch in enumerate(b):
        if i == idx: 
            board += token
            if ptr + 1 < len(lst):
                ptr += 1
                idx = lst[ptr]
        else: board += ch
    return board

def print2d(board):
    for i in range(8):
        print(board[i*8:(i+1)*8])

if certain: psbls, token, opp = possibles(board, token, 1)
else: psbls, token, opp = possibles(board, token, 0)
print2d(possiblesboard(board, psbls))
print()
print(board + " " + str(board.count("x")) + "/" + str(board.count("o")))
if len(psbls) > 0:
    print("Possible moves for " + token + ":", end = " ")
    for i in range(len(psbls) - 1):
        print(str(psbls[i])+", ", end = "")
    print(str(psbls[len(psbls) - 1]))
    print()
else: 
    print("No moves possible")
    print()
for i in range(len(moves)):
    print(token + " plays to " + str(moves[i]))
    board = makemove(board, token, opp, moves[i])
    psbls, token, opp = possibles(board, opp, 0)
    print2d(possiblesboard(board, psbls))
    print()
    print(board + " " + str(board.count("x")) + "/" + str(board.count("o")))
    if len(psbls) > 0:
        print("Possible moves for " + token + ":", end = " ")
        for i in range(len(psbls) - 1):
            print(str(psbls[i])+", ", end = "")
        print(str(psbls[len(psbls) - 1]))
        print()
# Neha Reddy, Pd4, 2024