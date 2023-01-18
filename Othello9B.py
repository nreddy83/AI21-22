import sys; args = sys.argv[1:]
# Neha Reddy
LIMIT_AB = 15
import time, random
chars = "ABCDEFGH"
nums = "1234567890"
board = ""
token = ""
certain = True
moves = [] # not needed for part aa
for ar in args: # initializes arguments passed in
    if "2024nreddy" in ar: continue
    elif len(ar) == 64 and ("." in ar or "x" in ar or "o" in ar): board = ar.lower()
    elif len(ar) >= 2 and ("0" in ar or "1" in ar or "2" in ar or "3" in ar or "4" in ar or "5" in ar or "6" in ar or "7" in ar or "8" in ar or "9" in ar):
        for val in range(0, len(ar), 2):
            mv = ar[val:val+2]
            if "_" in mv: mv = mv[1]
            imv = int(mv)
            if imv >= -1: moves.append(imv)
    elif ar in "xXOo": token = ar.lower()
    elif len(ar) > 0 and ar[0].upper() in chars: moves.append(int(chars.find(ar[0].upper()))+(int((ar[1])) - 1)*8)
    elif len(ar) > 0 and ar[0] in nums and int(ar) >= -1: moves.append(int(ar))
if board == "": board = "."*27 + "ox......xo" + "."*27
if token == "": 
    certain = False
    if board.count(".") % 2 == 1: token = "o"
    else: token = "x"

cacheMove = {}
def possibles(board, token, run):
    key = (board, token)
    if key in cacheMove: return cacheMove[key]
    #start with all of the empty tokens and check
    if token == "x": opp = "o"
    else: opp = "x"
    lst = []
    for i in range(len(board)):
        if board[i] == ".":
            # north
            if i//8 != 0:
                pos = i - 8
                ct = 0
                while pos > 0 and board[pos] == opp:
                    pos -= 8
                    ct += 1
                if pos >= 0 and ct > 0 and board[pos] == token and pos not in lst: 
                    lst.append(i)
                    continue
            # south
            if i//8 != 7:
                pos = i + 8
                ct = 0
                while pos < 64 and board[pos] == opp:
                    pos += 8
                    ct += 1
                if pos < 64 and ct > 0 and board[pos] == token and pos not in lst: 
                    lst.append(i)
                    continue
            # west
            if i%8 != 0:
                pos = i - 1
                ct = 0
                while pos%8 > 0 and pos > 0 and board[pos] == opp:
                    pos -= 1
                    ct += 1
                if pos >= 0 and pos%8 >= 0 and ct > 0 and board[pos] == token and pos not in lst: 
                    lst.append(i)
                    continue
            # east
            if i%8 != 7:
                pos = i + 1
                ct = 0
                while pos%8 < 7 and pos < 64 and board[pos] == opp:
                    pos += 1
                    ct += 1
                if pos < 64 and pos%8 <= 7 and ct > 0 and board[pos] == token and pos not in lst: 
                    lst.append(i)
                    continue
            # northwest
            if i//8 != 0 and i%8 != 0:
                pos = i - 9
                ct = 0
                while pos%8 > 0 and pos > 0 and board[pos] == opp:
                    pos -= 9
                    ct += 1
                if pos >= 0 and pos%8 >= 0 and ct > 0 and board[pos] == token and pos not in lst: 
                    lst.append(i)
                    continue
            # northeast
            if i//8 != 0 and i%8 != 7:
                pos = i - 7
                ct = 0
                while pos%8 < 7 and pos > 0 and board[pos] == opp:
                    pos -= 7
                    ct += 1
                if pos >= 0 and pos%8 <= 7 and ct > 0 and board[pos] == token and pos not in lst: 
                    lst.append(i)
                    continue
            # southwest 
            if i//8 != 7 and i%8 != 7:
                pos = i + 9
                ct = 0
                while pos%8 < 7 and pos < 64 and board[pos] == opp:
                    pos += 9
                    ct += 1
                if pos < 64 and pos%8 <= 7 and ct > 0 and board[pos] == token and pos not in lst: 
                    lst.append(i)
                    continue
            # southeast
            if i//8 != 7 and i%8 != 0:
                pos = i + 7
                ct = 0
                while pos%8 > 0 and pos < 64 and board[pos] == opp:
                    pos += 7
                    ct += 1
                if pos < 64 and pos%8 >= 0 and ct > 0 and board[pos] == token and pos not in lst: 
                    lst.append(i)
                    continue
    if len(lst) > 0: 
        cacheMove[key] = (lst, token, opp)
        return lst, token, opp
    if run == 0: 
        newlst, newopp, newtkn = possibles(board, opp, 1)
        if len(newlst) > 0: 
            cacheMove[key] = ([-1], token, opp)
            return [-1], token, opp
    cacheMove[key] = ([], opp, token)
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

def bestpossible(b, token, psbls):
    if token == "x": opp = "o"
    else: opp = "x"
    #if token == "o" and b[50] == "x" and 52 in psbls: return 52
    least = 9999
    midx = psbls[len(psbls)-1]
    e1 = [*range(8)]
    ct1 = 0
    for pos in e1:
        if b[pos] != ".": ct1 += 1
    e2 = [*range(56, 64)]
    ct2 = 0
    for pos in e2:
        if b[pos] != ".": ct2 += 1
    e3 = [*range(0, 57, 8)]
    ct3 = 0
    for pos in e3:
        if b[pos] != ".": ct3 += 1
    e4 = [*range(7, 64, 8)]
    ct4 = 0
    for pos in e4:
        if b[pos] != ".": ct4 += 1
    for lstpos, idx in enumerate(psbls):
        if idx in {0, 7, 56, 63}: return idx #corner
        if idx in e1 and (ct1 == 7 or (b[e1.index(idx) - 1] == opp and b[e1.index(idx) + 1] == opp)): return idx #safe edge moves
        if idx in e2 and (ct2 == 7 or (b[e2.index(idx) - 1] == opp and b[e2.index(idx) + 1] == opp)): return idx #safe edge moves
        if idx in e3 and (ct3 == 7 or (b[e3.index(idx) - 1] == opp and b[e3.index(idx) + 1] == opp)): return idx #safe edge moves
        if idx in e4 and (ct4 == 7 or (b[e4.index(idx) - 1] == opp and b[e4.index(idx) + 1] == opp)): return idx #safe edge moves
        if idx in {1, 8, 9}:
            if b[0] != token: continue #avoiding cx moves
        if idx in {6, 14, 15}:
            if b[7] != token: continue #avoiding cx moves
        if idx in {48, 49, 57}: 
            if b[56] != token: continue #avoiding cx moves
        if idx in {54, 55, 62}: 
            if b[63] != token: continue #avoiding cx moves
        board = makemove(b, token, opp, idx)
        moves, t, o = possibles(board, opp, 0)
        if len(moves) > 0 and moves[0] == -1: continue
        if len(moves) == 0: return idx
        if len(moves) < least: #least mobility
            least = len(moves)
            midx = idx
    return midx

cachemm = {}
def makemove(board, token, opp, position):
    key = (board, token, position)
    if key in cachemm: return cachemm[key]
    if position == -1: 
        cachemm[key] = board
        return board
    if board.count(".") == 0: 
        cachemm[key] = board
        return board
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
                mm = move(board, token, fin)
                cachemm[key] = mm
                return mm
    cachemm[key] = ""
    return ""

def move(b, token, lst):
    if len(lst) == 0: return b
    board = [*b]
    for i in lst:
        board[i] = token
    return "".join(board)

def score(board, tkn): ##
    sc = 0
    return sc

def m_alphabeta(board, tkn, curr, depth, sc):
    if tkn == "x": opp = "o"
    else: opp = "x"
    psbls, tk, op = possibles(board, tkn, 0)
    if curr == depth:
        return sc + score(board, tkn)
    if curr == 1:
        for idx in psbls:
            e1 = [*range(8)]
            ct1 = 0
            for pos in e1:
                if board[pos] != ".": ct1 += 1
            e2 = [*range(56, 64)]
            ct2 = 0
            for pos in e2:
                if board[pos] != ".": ct2 += 1
            e3 = [*range(0, 57, 8)]
            ct3 = 0
            for pos in e3:
                if board[pos] != ".": ct3 += 1
            e4 = [*range(7, 64, 8)]
            ct4 = 0
            for pos in e4:
                if board[pos] != ".": ct4 += 1
            for lstpos, idx in enumerate(psbls):
                if idx in {0, 7, 56, 63}: sc += 100 #corner
                if idx in e1 and (ct1 == 7 or (board[e1.index(idx) - 1] == opp and board[e1.index(idx) + 1] == opp)): sc += 20 #safe edge moves
                if idx in e2 and (ct2 == 7 or (board[e2.index(idx) - 1] == opp and board[e2.index(idx) + 1] == opp)): sc += 20 #safe edge moves
                if idx in e3 and (ct3 == 7 or (board[e3.index(idx) - 1] == opp and board[e3.index(idx) + 1] == opp)): sc += 20 #safe edge moves
                if idx in e4 and (ct4 == 7 or (board[e4.index(idx) - 1] == opp and board[e4.index(idx) + 1] == opp)): sc += 20 #safe edge moves
                if idx in {1, 8, 9}:
                    if board[0] != token: sc -= 100 #avoiding cx moves
                if idx in {6, 14, 15}:
                    if board[7] != token: sc -= 100 #avoiding cx moves
                if idx in {48, 49, 57}: 
                    if board[56] != token: sc -= 100 #avoiding cx moves
                if idx in {54, 55, 62}: 
                    if board[63] != token: sc -= 100 #avoiding cx moves
    for mv in psbls:
        board = makemove(board, tkn, opp, mv)
        return m_alphabeta(board, opp, curr+1, depth)
    
def t_alphabeta(board, tkn, alpha, beta): #using negamax, terminal alpha beta
    if tkn == "x": opp = "o"
    else: opp = "x"
    psbls, tk, op = possibles(board, tkn, 0)
    if len(psbls) == 0:
        score = board.count(tkn)-board.count(opp)
        if len(psbls) == 0: return [score]
        ab = t_alphabeta(board,opp,-beta, -alpha)
        return [-ab[0]] + ab[1:]
    best = [alpha-1]
    for mv in psbls:
        nm = t_alphabeta(makemove(board,tkn,opp,mv), opp, -beta, -alpha)
        score = -nm[0]
        if score < alpha: continue
        if score > beta: return [score]
        best = [-nm[0]] + nm[1:] + [mv]
        alpha = score + 1
    return best

def quickMove(board, token):
    psbls, token, opp = possibles(board, token, 0)
    return bestpossible(board, token, psbls)

def print2d(board):
    for i in range(8):
        print(board[i*8:(i+1)*8])

def main():
    global board, token, moves
    if len(args) == 0:
        begin = time.process_time()
        game = 1
        mytk = 0
        tottk = 0
        s1, g1, q1, t1 = 65, 0, "", "x"
        s2, g2, q2, t2 = 65, 0, "", "x"
        while game <= 100:
            board = "."*27 + "ox......xo" + "."*27
            if (game%2) == 1: token = "x"
            else: token = "o"
            tk = "x"
            seq = ""
            while board.count(".") != 0:
                psbls, tk, op = possibles(board, tk, 0)
                if len(psbls) == 0: break
                if tk != token:
                    n = random.randint(0, len(psbls) - 1)
                    mv = psbls[n]
                    # mv = bestpossible(board, tk, psbls)
                    # if board.count(".") < LIMIT_AB:
                    #     sq = t_alphabeta(board, tk, -64, 64)
                    #     mv = int(sq[len(sq) - 1])
                else:
                    mv = bestpossible(board, tk, psbls)
                    # mv = m_alphabeta(board, tk, 1, 5, 0)
                    if board.count(".") < LIMIT_AB:
                        sq = t_alphabeta(board, tk, -64, 64)
                        mv = int(sq[len(sq) - 1])
                ms = str(mv)
                if len(ms) == 1: seq += "_" + ms
                else: seq += ms
                board = makemove(board, tk, op, mv)
                tk = op
            if token == "o": opp = "x"
            else: opp = "o"
            tcount = board.count(token)
            ocount = board.count(opp)
            tot = tcount + ocount
            diff = tcount - ocount
            if s1 == 65 or (s1 < 65 and s2 <= s1 and diff < s1): 
                s1 = diff
                g1 = game
                q1 = seq
                t1 = token
            elif s2 == 65 or (s2 < 65 and s1 <= s2 and diff < s2):
                s2 = diff
                g2 = game
                q2 = seq
                t2 = token
            print(diff, end = " ")
            if game%10 == 0: print()
            game += 1
            mytk += tcount
            tottk += tot
        print("My tokens:", mytk, "Total tokens:", tottk)
        score = format(mytk*100/tottk, ".1f") + "%"
        print("Score:", score)
        print("NM/AB LIMIT:", LIMIT_AB)
        print("Game", str(g1), "as", t1, " =>", str(s1))
        print(q1)
        print("Game", str(g2), "as", t2, " =>", str(s2))
        print(q2)
        print("Elapsed time:", format(abs(begin - time.process_time()), ".2f") + "s")
    else:
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
            print("Quick move:", quickMove(board, token))
            print()
        else: 
            print("No moves possible")
            print()
        for i in range(len(moves)):
            print(token + " plays to " + str(moves[i]))
            board = makemove(board, token, opp, moves[i])
            psbls, token, opp = possibles(board, opp, 0)
            if psbls != [-1]: print2d(possiblesboard(board, psbls))
            else:
                npsbls, ntoken, nopp = possibles(board, opp, 0)
                print2d(possiblesboard(board, npsbls))
            print()
            print(board + " " + str(board.count("x")) + "/" + str(board.count("o")))
            if len(psbls) > 0:
                if psbls != [-1]:
                    print("Possible moves for " + token + ":", end = " ")
                    for i in range(len(psbls) - 1):
                        print(str(psbls[i])+ ", ", end = "")
                    print(str(psbls[len(psbls) - 1]))
                    print("Quick move:", quickMove(board, token))
                    print()
                else: 
                    print("Possible moves for " + ntoken + ":", end = " ")
                    for i in range(len(npsbls) - 1):
                        print(str(npsbls[i])+ ", ", end = "")
                    print(str(npsbls[len(npsbls) - 1]))
                    print("Quick move:", quickMove(board, ntoken))
                    print()
        begin = time.process_time()
        if board.count(".") < LIMIT_AB: 
            lst = t_alphabeta(board, token, -64, 64)
            print("score:", lst)
            print(format(abs(time.process_time() - begin), ".2f"))
if __name__ == '__main__': main()

class Strategy:
    logging = True
    def best_strategy(self, board, player, best_move, running):
        if running.value:
            best_move.value = quickMove(board, player)
        if board.count(".") < LIMIT_AB:
            sq = t_alphabeta(board, player, -64, 64)
            best_move.value = int(sq[len(sq) - 1])
# Neha Reddy, Pd4, 2024