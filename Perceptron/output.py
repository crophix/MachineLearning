numEpochs = {}
learningRate = 0
trainAcc = {}
testAcc = {}
confMat = {}

for i in range(10):
    for j in range(i+1,10):
        trainAcc[str(i)+str(j)] = 0.0
        numEpochs[str(i)+str(j)] = 1
        testAcc[str(i)+str(j)] = 0.0
        confMat[str(i)+str(j)] = {'TP':0, 'TN':0, 'FP':0, 'FN':0}

def outputData():
    print "\\documentclass[11pt]{article}"
    print "\\usepackage{amsmath,amssymb}"
    print "\\author{Daniel Leblanc}"
    print "\\title{Discrete-event Simulation \\ Assignment 2}"
    print "\\date{April 25, 2013}"
    print "\\begin{document}"
    print "\\maketitle"
    for key in sorted(numEpochs.keys()):
        print "\\begin{center}"
        print "\\begin{tabular}{l | r r}"
        print "Perceptron &&" + key + "\\\\"
        print "Number of Epochs & &"+ str(numEpochs[key]) + "\\\\"
        print "Training Accuracy & &"+ "%.3f" % trainAcc[key] + "\\\\"
        print "Test Accuracy & &"+ "%.3f" % testAcc[key] + "\\\\"
        print "Confusion Matrix &"+ str(confMat[key]['TP']) + ' & ' + str(confMat[key]['FP'])+ "\\\\"
        print " &" + str(confMat[key]['FN']) + ' & ' + str(confMat[key]['TN'])+ "\\\\"
        print "\\end{tabular}"
        print "\\end{center}"
    print "\\end{document}"
