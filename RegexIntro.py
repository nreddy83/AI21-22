import sys; args = sys.argv[1:]
idx = int(args[0])-30

#total len: 143, best len: 143

myRegexLst = [r"/^0$|^10[01]$/", #30
r"/^[01]*$/", #31
r"/^[01]*0$/", #32
r"/\w*[aeiou]\w*[aeiou]\w*/i", #33
r"/^0$|^1[01]*0$/", #34
r"/^[01]*110[01]*$/", #35
r"/^.{2,4}$/s", #36
r"/^\d{3} *-? *\d\d *-? *\d{4}$/", #37
r"/^.*?d\w*/im", #38
r"/^0[01]*0$|^1[01]*1$|^[01]?$/"] #39

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Neha Reddy, Pd 4, 2024