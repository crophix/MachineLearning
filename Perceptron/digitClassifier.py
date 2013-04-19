from __future__ import division  #import real number division
from perceptron import *

perceptrons = {}
learningRate = 0.2

def createPerceptrons():
    """Initializes the 45 perceptrons"""
    global perceptrons
    for i in range(10):
        for j in range(i+1,10):
            perceptrons[str(i)+str(j)] = Perceptron()

def getData(fname):
    """Retrieves the training data from optdigits.train and stores
    the data in a dict sorted by the classifier"""
    entries = {}
    for i in range(10):
        entries[i] = []
    with open(fname) as f:
        for line in f:
            index = int(line.split(',')[-1])
            entries[index].append(line.split(','))
    return entries

def runEpoch(trainingData):
    """This runs the training data through the perceptrons for 
    a single epoch and returns the accuracy.  The trainingData
    is a dict of attributes sorted by actual classification.
    """
    global perceptrons
    correct = 0
    total = 0
    for digit, data in trainingData.items():
        for d in data:
            for i in range(10):
                if i < digit:
                    c = perceptrons[str(i)+str(digit)].train(learningRate,d,-1)
                    if c == -1:
                        correct += 1
                    total += 1
                elif i > digit:
                    c = perceptrons[str(digit)+str(i)].train(learningRate,d,1)
                    if c == 1:
                        correct += 1
                    total += 1
    return correct / total

def testPerceptrons():
    testData = getData('optdigits.test')
    cl = {}
    for i in range(10):
        cl[i] = {}
        for j in range(10):
            cl[i][j] = 0
    for digit, data in trainingData.items():
        for d in data:
            for i in range(10):
                if i < digit:
                    c = perceptrons[str(i)+str(digit)].train(learningRate,d,-1)
                    if c == -1:
                        cl[digit][digit] += 1
                    else:
                        cl[digit][i] += 1
                elif i > digit:
                    c = perceptrons[str(digit)+str(i)].train(learningRate,d,1)
                    if c == 1:
                        cl[digit][digit] += 1
                    else:
                        cl[digit][i] += 1
    return cl

if __name__ == "__main__":
    createPerceptrons()
    trainingData = getData('optdigits.train')
    lastAcc = 0
    runs = 1
    curAcc = runEpoch(trainingData)
    while curAcc > lastAcc:
        lastAcc = curAcc
        curAcc = runEpoch(trainingData)
        runs += 1
    print curAcc, lastAcc, runs
    cl = testPerceptrons()
    for i in range(10):
        print cl[i]
