import subprocess as sub
import random
import math

K = 20 #number of boosting iterations

# Read in the training data and set the weights to their default value
trainData = []
with open('spam.train') as f:
    for l in f:
        trainData.append({'d':l})
for t in trainData:
    t['w'] = 1.0/len(trainData)

# Randomly build the first set of training data and write the data to a file
S = []
while len(S) < len(trainData):
    S.append(random.randint(0, len(trainData)-1))
S.sort()
with open('spam.temp', 'w+') as f:
    for s in S:
        f.write(trainData[s]['d'])

a = []
for i in range(K):
    e = []
    # Run svm-light on the training set to build a model
    sub.call(['./svm_learn', '-t', '0', 'spam.temp', 'spam.model' + str(i)])
    # Test the accuracy of the model and calculate the error
    sub.call(['./svm_classify', 'spam.train', 'spam.model' + str(i), 'spam.predictions' + str(i)])
    with open('spam.predictions' + str(i)) as f:
        for t in trainData:
            if t['d'][0] == '-':
                if f.readline().lstrip()[0] == '-':
                    e.append(0.0)
                else:
                    e.append(t['w'])
            else:
                if f.readline().lstrip()[0] == '-':
                    e.append(t['w'])
                else:
                    e.append(0.0)
    totalE = sum(e)
    a.append(.5 * math.log((1-totalE)/totalE))
    # Adjust the weights on the training data
    Z = 0.0
    for j in range(len(trainData)):
        if e[j] != 0.0:
            x = 1
        else:
            x = -1
        trainData[j]['w'] = trainData[j]['w'] * math.exp(a[i]*x)
        Z += trainData[j]['w']
    for t in trainData:
        t['w'] = t['w'] / Z
    # Build a new set of training data using the adjusted weights   
    S = []
    for j in range(len(trainData)):
        choice = random.random()
        total = trainData[0]['w']
        index = 0
        while total < choice:
            total += trainData[index+1]['w']
            index += 1
        S.append(index)
    S.sort()
    with open('spam.temp', 'w+') as f:
        for s in S:
            f.write(trainData[s]['d'])

# Analyze the test data using the various hypothesis
for i in range(K):
    sub.call(['./svm_classify', 'spam.test', 'spam.model' + str(i), 'spam.predictions' + str(i)])

# Adjust the predictions by the alpha value and generate a new predictions file
total = [0.0 for x in range(3681)]
for i in range(K):
    with open('spam.predictions' + str(i)) as f:
        for j in range(3681):
            if f.readline().strip()[0] == '-':
                total[j] -= a[i]
            else:
                total[j] += a[i]

with open('spam.predictions', 'w+') as f:
    for i in range(3681):
        d = total[i]
        f.write(str(d) + '\n')
