import sys; args = sys.argv[1:]

cacheChange = {} #to avoid recomputation

#state recursion example - AVOID RECOMPUTATION IN OTHELLO5
def change(amount, coinlist):
    key = (amount, *coinlist)
    if key in cacheChange: return cacheChange[key]
    if amount <= 0: returnVal = amount==0
    elif not coinlist: returnVal = 0
    else: returnVal = change(amount-coinlist[0], coinlist) + change(amount, coinlist[1:])
    cacheChange[key] = returnVal
    return returnVal

print(change(10000, [100, 50, 25, 10, 5, 1]))