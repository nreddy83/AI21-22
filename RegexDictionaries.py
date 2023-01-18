import sys; args = sys.argv[1:]
idx = int(args[0])-70

#total len: 260, best len: 246

myRegexLst = [r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)[a-z]*u\w*$/m", #70 - 40
r"/^([^\WA-aeiou]*[aeiou]){5}[^\Waeiou]*$/m", #71 - 38
r"/^(?=.*[^\Waeiou]w[^aeiou]{2})[a-z]/m", #72 - 34
r"/^(a*|(?=([a-z])(.)(\w)).*\4\3\2)$/m", #73 - 33
r"/^[ac-su-z]*(bt|tb)[^\Wbt]*$/m", #74 - 27
r"/^([a-z])*\1\w*$/m", #75 - 15
r"/(.).*(\1\w*){5}$/m", #76 - 16
r"/((.)\2){3}\w*$/m", #77 - 14
r"/(\w*[^\Waeiou]){13}/m", #78 - 19
r"/^(?!(.)*.*\1.*\1)[a-z]+$/m"] #79 - 24

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Neha Reddy, Pd 4, 2024