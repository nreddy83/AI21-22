import sys; args = sys.argv[1:]
idx = int(args[0])-50

#total len: 196, best len: 189

myRegexLst = [r"/(\w)*\w*\1\w*/i", #50 
r"/(\w)*(\w*\1){3}\w*/i", #51 
r"/^(0|1)([01]*\1)*$/", #52
r"/\b(?=\w*cat)\w{6}\b/i", #53
r"/\b(?=\w*ing)(?=\w*bri)\w{5,9}\b/i", #54
r"/\b(?!\w*cat)\w{6}\b/i", #55
r"/\b(?!(\w)*\w*\1)\w+/i", #56
r"/^(?!.*10011)[01]*$/", #57
r"/\w*(([aeiou])(?!\2)){2}\w*/i", #58
r"/^(?!.*1.1)[01]*$/"] #59

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Neha Reddy, Pd 4, 2024