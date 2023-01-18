import sys; args = sys.argv[1:]
idx = int(args[0])-40

#total len: 181, best len: 181

myRegexLst = [r"/^[.xo]{64}$/i", #40
r"/^[xo]*\.[xo]*$/i", #41
r"/^(x+o*)?\.|\.(o*x+)?$/i", #42
r"/^.(..)*$/s", #43
r"/^(1?0|11)([01]{2})*$/", #44
r"/\w*([aeio]u|[aeiu]o|[aeou]i|[aiou]e|[eiou]a)\w*/i", #45
r"/^(1?0)*1*/", #46
r"/^\b[bc]*a?[bc]*$/", #47
r"/^(b|c|a[bc]*a)+$/", #48
r"/^((2|1[^1]*1)0*)+$/"] #49

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Neha Reddy, Pd 4, 2024