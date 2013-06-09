import random

class Perceptron:
    def __init__(self, numInputs, learningRate):
        self.bias = random.uniform(-1,1)
        self.inputs = []
        for i in range(numInputs):
            self.inputs.append(random.uniform(-1,1))
        self.acc = [0.0, 0.0, 0.0] #[accuracy before epoch, accuracy after epoch, testing accuracy]
        self.runs = 0
        self.confMat = [0, 0, 0, 0] #[TP, FP, TN, FN]
        self.finished = False
        self.learningRate = learningRate
        
    def classify(self, data):
        total = self.bias
        for i in range(len(self.inputs)):
            total += self.inputs[i] * data[i]
        return total
        
    def train(self, data, output):
        self.bias += self.learningRate * -2 * output
        for i in range(len(self.inputs)):
            self.input[i] += self.learningRate * -2 * output * data[i]

perceptrons = {}
for i in range(10):
    for j in range(10):
        key = 'p' + str(i) + str(j)
        perceptrons[key] = Perceptron(64, 0.2)
        
running = True
while running:
    running = False
    