from __future__ import division  #import real number division
from perceptron import *
import formatOutput

perceptrons = {}
learningRate = 0.2

def createPerceptrons():
    """Initializes the 45 perceptrons
    """
    global perceptrons
    for i in range(10):
        for j in range(i+1,10):
            perceptrons[str(i)+str(j)] = Perceptron()

def getData(fname):
    """Retrieves the training data from optdigits.train and stores
    the data in a dict sorted by the classifier
    """
    entries = {}
    for i in range(10):
        entries[i] = []
    with open(fname) as f:
        for line in f:
            index = int(line.split(',')[-1])
            entries[index].append(line.split(','))
    return entries

def runEpoch(trainingData, key):
    """This runs the training data through the given perceptron for 
    a single epoch and returns the accuracy.  The trainingData
    is a dict of attributes sorted by actual classification.
    """
    global perceptrons
    correct = 0
    total = 0
    for digit, data in trainingData.items():
        for d in data:
            if str(digit) == key[0]:
                expected = -1
            elif str(digit) == key[1]:
                expected = 1
            else:
                break
            c = perceptrons[key].train(learningRate,d,expected)
            if c == expected:
                correct += 1
            total += 1
    return correct / total

def testPerceptrons(testData, key):
    """Runs the testData through the given perceptron and returns the accuracy
    and the number of classifications of each type
    """
    cl = {}
    for i in range(10):
        cl[i] = {}
        for j in range(10):
            cl[i][j] = 0
    for digit, data in testData.items():
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
    lastAcc = {}
    runs = {}
    for key in perceptrons.keys():
        lastAcc[key] = 0
        runs[key] = 1
    for key in sorted(perceptrons.keys()):
        curAcc = runEpoch(trainingData, key)
        while curAcc > lastAcc[key]:
            lastAcc[key] = curAcc
            curAcc = runEpoch(trainingData, key)
            runs[key] += 1
        print key, curAcc, lastAcc[key], runs[key]
    testData = getData('optdigits.test')
    testAcc = {}
    numRight = {}
    numWrong = {}
    for key in perceptrons.keys():
        testAcc[key] = 0
    for key in sorted(perceptrons.keys():
        testAcc[key] = testPerceptrons(testData, key)        
        print testAcc[key]
