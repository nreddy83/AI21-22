import sys; args = sys.argv[1:]
from math import pi, acos, sin, cos

# maps each station to its latitude and longitude
myNodes = open("rrNodes.txt", "r").read().splitlines()
dctCoords = {}  # station:(latitude, longitude)
for node in myNodes:
    if node not in dctCoords:
        station = node[:node.find(" ")]
        lat = float(node[node.find(" ") + 1:node.find("-") - 1])
        long = float(node[node.find("-"):])
        dctCoords[station] = (lat, long)

# makes the edges/neighbors dct
myEdges = open("rrEdges.txt", "r").read().splitlines()
dctEdges = {}  # station: list of neighbors
for node in myEdges:
    station1 = node[:node.find(" ")]
    station2 = node[node.find(" ") + 1:]
    if station1 in dctEdges and station2 not in dctEdges[station1]:
        dctEdges[station1].append(station2)
    if station1 not in dctEdges:
        dctEdges[station1] = [station2]
    if station2 in dctEdges and station1 not in dctEdges[station2]:
        dctEdges[station2].append(station1)
    if station2 not in dctEdges:
        dctEdges[station2] = [station1]

# maps the station number to the city name if there is one
myCities = open("rrNodeCity.txt", "r").read().splitlines()
dctCities = {}  # station: city
for node in myCities:
    if node not in dctCities:
        station = node[:node.find(" ")]
        city = node[node.find(" ") + 1:]
        dctCities[station] = city

city1 = args[0]
city2 = args[1]
if city1.isalpha() and city1 not in dctCities.values():
    city1 = args[0] + " " + args[1]
    city2 = args[2]
    if city2.isalpha() and city2 not in dctCities.values(): city2 = args[2] + " " + args[3]
elif city1.isalpha() and city1 in dctCities.values() and city2.isalpha() and city2 not in dctCities.values(): city2 = args[1] + " " + args[2]
elif city1.isalpha() and city1 not in dctCities.values():
    city1 = args[0] + " " + args[1]
    city2 = args[2]
for city in dctCities:
    if dctCities[city] == city1: city1 = city
    if dctCities[city] == city2: city2 = city

# heuristic estimate
def calcd(y1, x1, y2, x2):
    # y1 = lat1, x1 = long1, y2 = lat2, x2 = long2, all assumed to be in decimal degrees
    R = 3958.76  # miles = 6371 km
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0
    # approximate great circle distance with law of cosines
    if abs(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) < 1: return acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1))*R
    else: return 9999


def aStar(start, goal):
    if start == goal: return "same location"
    closedSet = {}  # child:parent
    ystart, xstart = dctCoords[start]
    ygoal, xgoal = dctCoords[goal]
    openSet = [(calcd(ystart, xstart, ygoal, xgoal), start, "n/a")]  # est, dist curr, node, parents
    while openSet:
        d, node, child = min(openSet)
        openSet.remove((d, node, child))
        if node in closedSet: continue
        closedSet[node] = child
        if node == goal: return find_path(closedSet)
        for nbr in dctEdges[node]:
            if nbr in closedSet: continue
            y1, x1 = dctCoords[node]
            y2, x2 = dctCoords[nbr]
            openSet.append(((d + calcd(y1, x1, y2, x2) + calcd(y2, x2, ygoal, xgoal) - (calcd(y1, x1, ygoal, xgoal))), nbr, node))


# takes in the dictionary from AStar and retrieves the pathLst backwards
def find_path(dct):
    path = []
    node = city2
    dist1 = 0.0
    steps = 0
    while node != "n/a":
        if node in dctCities: path.append(dctCities[node])
        else: path.append(node)
        if dct[node] != "n/a":
            y1, x1 = dctCoords[node]
            y2, x2 = dctCoords[dct[node]]
            dist1 += calcd(y1, x1, y2, x2)
        steps += 1
        node = dct[node]
    return path, dist1, steps - 1


pathLst, dist, steps = aStar(city1, city2)
path = ""
for ind in range(len(pathLst)):
    path += pathLst[len(pathLst) - 1 - ind] + " "
print("Path:", path)
print("Distance:", dist)
print("Number of Stops:", steps)

# Neha Reddy, Pd 4, 2024