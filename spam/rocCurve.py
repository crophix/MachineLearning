import numpy as np
import pylab as pl

#Read in the test data to determine the break between spam and non-spam
lineNum = 0
with open('spam.test') as f: 
    for l in f:
        lineNum += 1
        if l.lstrip()[0] == '-':  #Stop when we reach the first negative instance
            break

#Read the results from the predictions file and sort into spam/non-spam lists
notSpam = []
spam = []
c = 0
with open('spam.predictions') as f:
    for l in f:
        c += 1
        if c < lineNum:
            spam.append(float(l))
        else:
            notSpam.append(float(l))

#Sort the lists to find min and max values
notSpam.sort()
spam.sort()

tp = 0
tn = 0
for s in spam:
    if s > 0:
        tp += 1
for s in notSpam:
    if s < 0:
        tn += 1 
print "accuracy:", float(tp + tn)/c

# Setup a list of evenly spaced thresholds for the ROC curve
rocPoint = []
rocPoint.append(c / 21)
for i in range(1,20):
    rocPoint.append(rocPoint[i-1] + (c / 21))

data = [{'TP':0, 'FP': 0, 'TN':0, 'FN':0} for x in range(20)]
for i in range(c):
    # Get the max value from the spam and non-spam lists
    try:
        a = notSpam[-1]
    except IndexError:
        a = min(spam)-1
    try:
        b = spam[-1]
    except IndexError:
        b = min(notSpam)-1
    # Pop the larger value and adjust the data
    if b > a:
        spam.pop()
        for j in range(20):
            if i >= rocPoint[j]:
                data[j]['TP'] += 1
            else:
                data[j]['FN'] += 1
    else:
        notSpam.pop()
        for j in range(20):
            if i >= rocPoint[j]:
                data[j]['FP'] += 1
            else:
                data[j]['TN'] += 1

# Generate lists of the x and y values for the graph
tpr = []
fpr = []
for i in range(20):
    tpr.append(float(data[i]['TP']) / (data[i]['TP'] + data[i]['FN']))
    fpr.append(float(data[i]['FP']) / (data[i]['FP'] + data[i]['TN']))
# Plot the data and label the graph
pl.plot(tpr, fpr, 'r^-')
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('ROC Curve')
pl.xlim(0, 1.0)
pl.ylim(0, 1.0)
pl.show() # Display the results
