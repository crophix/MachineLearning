from __future__ import division
from math import *
from random import *
from copy import deepcopy

import visualize

class cluster:
    def __init__(self):
        self.centroid = [randint(0,16) for x in range(64)]
        self.data = []
        self.dist = []
        self.type = 0
        self.SSE = 0
    
    def distance(self, d, sqrt=True):
        if sqrt:
            return sum([(d[x] - self.centroid[x])**2 for x in range(64)])**0.5
        return sum([(d[x] - self.centroid[x])**2 for x in range(64)])
        
    def add(self, d):
        self.data.append(d)
        self.dist.append(self.distance(d))
        self.SSE += self.distance(d, False)
        
    def moveCntr(self):
        if len(self.data) == 0:
            return False
        self.centroid = [0 for x in range(64)]
        for d in self.data:
            for i in range(64):
                self.centroid[i] += d[i]
        for i in range(64):
            self.centroid[i] = self.centroid[i]/len(self.data)
        return True
    
    def clearData(self):
        self.data = []
        self.dist = []
        self.SSE = 0
        
    def computeType(self):
        types = [0 for x in range(10)]
        for d in self.data:
            types[d[-1]] += 1
        self.type = types.index(max(types))
        
    def furthestItem(self):
        if len(self.data) == 0:
            return [], 0
        i = self.dist.index(max(self.dist))
        return self.data[i], self.dist[i]

K = 10      #number of centroids

data = []
with open('optdigits.train') as f:
    for line in f:        
        data.append([int(x) for x in line.split(',')])
        
clusters = [cluster() for x in range(K)]
        
bestCntrs = [deepcopy(clusters[x].centroid) for x in range(K)]
bestSSE = 10000000000
for i in range(5):
    count = 0
    seen = []
    clusters = [cluster() for x in range(K)]
    while [clusters[x].centroid for x in range(K)] not in seen:
        count += 1
        seen.append([deepcopy(clusters[x].centroid) for x in range(K)])
        for c in clusters:
            c.clearData()
        for d in data:
            closest = 0
            minDist = 16*64
            for i in range(K):
                dist = clusters[i].distance(d)
                if dist < minDist:
                    minDist = dist
                    closest = i
            clusters[closest].add(d)
        for c in clusters:
            if not c.moveCntr():
                d = []
                maxD = 0
                for x in clusters:
                    dat, dist = x.furthestItem()
                    if maxD < dist:
                        maxD = dist
                        d = dat
                c.add(d)
                c.moveCntr()
                
    for c in clusters:
        c.clearData()
    for d in data:
            closest = 0
            minDist = 16*64
            for i in range(K):
                dist = clusters[i].distance(d)
                if dist < minDist:
                    minDist = dist
                    closest = i
            clusters[closest].add(d)
    SSE = sum([clusters[x].SSE for x in range(K)])
    if SSE < bestSSE:
        bestSSE = SSE
        bestCntrs = [deepcopy(clusters[x].centroid) for x in range(K)]
    print SSE, count
    
    
for i in range(K):
    clusters[i].clearData()
    clusters[i].add(bestCntrs[i])
    clusters[i].moveCntr()
    clusters[i].clearData()
for d in data:
    closest = 0
    minDist = 16*64
    for i in range(K):
        dist = clusters[i].distance(d)
        if dist < minDist:
            minDist = dist
            closest = i
    clusters[closest].add(d)
for c in clusters:
    c.computeType()
    
confMat = [[0 for a in range(10)] for b in range(10)]
corCount = 0
count = 0
with open('optdigits.test') as f:
    for line in f:
        l = [int(x) for x in line.split(',')]
        type = 0
        minDist = 16*64
        for i in range(K):
            dist = clusters[i].distance(l)
            if dist <= minDist:
                minDist = dist
                type = clusters[i].type
        confMat[l[-1]][type] += 1
        if l[-1] == type:
            corCount += 1
        count += 1

visualize.makeImgs(bestCntrs)
for i in range(10):
    print confMat[i]
print "Accuracy:", corCount / count