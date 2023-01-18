import sys; args = sys.argv[1:]
from PIL import Image; img = Image.open(args[0])
import math
import random
k = int(args[1])

#loading in image and collecting basic image data
height = img.size[0]
width = img.size[1]
pix = img.load()

#initial stats
print("Size:", height ,"x", width)
print("Pixels:", height*width)
dis = {}
max_pix = (0, 0, 0)
max_val = 0

for h in range(height):
    for w in range(width):
        val = pix[h, w]
        if val in dis: dis[val].append((h, w))
        else: dis[val] = [(h, w)]
        if len(dis[val]) > max_val:
            max_val = len(dis[val])
            max_pix = val
print("Distinct pixel count:", len(dis))
print("Most common pixel:", max_pix, "->", max_val)
#kmeans
kmeans = [(random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255)) for i in range(k)]
buckets = {i: [] for i in range(k)}
places = {}

def distance(a, b):
    d = 0
    for i in range(3):
        d += (a[i] - b[i])*(a[i] - b[i])
    return math.sqrt(d)

def mindist(a, kmeans):
    mindist = 99999999999999999999
    minidx = 0
    for i in range(k):
        d = distance(a, kmeans[i])
        if d < mindist: 
            mindist = d
            minidx = i
    return minidx

def updatemeans(kmeans, buckets):
    for i, bucket in enumerate(buckets):
        tot = 0
        tot1 = 0
        tot2 = 0
        tot3 = 0
        for val in buckets[bucket]:
            v1, v2, v3 = val
            tot1 += v1
            tot2 += v2
            tot3 += v3
            tot += 1
        if tot != 0: kmeans[i] = (tot1/tot, tot2/tot, tot3/tot)
        else: kmeans[i] = (tot1, tot2, tot3)
    return kmeans

b = True
while(b):
    hopct = 0
    for p in dis:
        bucket = mindist(p, kmeans)
        for i in range(len(dis[p])):
            buckets[bucket].append(p)
        if p not in places: hopct = 10
        elif places[p] != bucket: hopct += 1
        places[p] = bucket
    kmeans = updatemeans(kmeans, buckets)
    if hopct == 0: 
        b = False
        continue
    for b in buckets:
        buckets[b] = []

print("Final means:")
for i in range(k):
    s = str(i+1) + ": " + str(kmeans[i]) + " => " + str(len(buckets[i]))
    print(s)

#remake image
for h in range(height):
    for w in range(width):
        v1, v2, v3 = kmeans[places[pix[h,w]]]
        if v1 % 1 >= 0.5: v1 = math.ceil(v1)
        else: v1 = math.floor(v1)
        if v2 % 1 >= 0.5: v2 = math.ceil(v2)
        else: v2 = math.floor(v2)
        if v3 % 1 >= 0.5: v3 = math.ceil(v3)
        else: v3 = math.floor(v3)
        kmeans[places[pix[h,w]]] = (v1, v2, v3)
        pix[h, w] = (v1, v2, v3)

img.save("kmeans/{}.png".format("2024nreddy"), "PNG")

def neighbors(p1, p2):
    nbrs = []
    if p1 > 0: nbrs.append((p1-1, p2))
    if p1 < height - 1: nbrs.append((p1+1, p2))
    if p2 > 0: nbrs.append((p1, p2-1))
    if p2 < width - 1: nbrs.append((p1, p2+1))
    if p1 > 0 and p2 > 0: nbrs.append((p1-1, p2-1))
    if p1 > 0 and p2 < width - 1: nbrs.append((p1-1, p2+1))
    if p1 < height - 1 and p2 > 0: nbrs.append((p1+1, p2-1))
    if p1 < height - 1 and p2 < width - 1: nbrs.append((p1+1, p2+1))
    return nbrs

#floodfill/region counts
region_counts = [0 for i in range(k)]
seen = set()
for h in range(height):
    for w in range(width):
        if (h, w) in seen: continue
        parseMe = [(h, w)]
        start = (h, w)
        v = pix[h, w]
        ind = kmeans.index(v)
        while parseMe:
            node = parseMe[0]
            for nbr in neighbors(node[0], node[1]):
                if pix[nbr[0], nbr[1]] != v: continue
                if nbr not in seen:
                    parseMe.append(nbr)
                    seen.add(nbr)
            parseMe.remove(node)
        region_counts[ind] += 1
    
string = "Region counts:"
for v in region_counts:
    string += " " + str(v)
print(string)
#Neha Reddy, Pd.4, 2024