#coding:utf-8
__author__ = 'lyj'
from numpy import *

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open(r'/Users/lyj/Programs/Codes&Data/machinelearninginaction/Ch05/testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])  #读取数据
        labelMat.append(int(lineArr[2]))   #读取标签
    return dataMat, labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500   #设置迭代次数
    weights = ones((n,1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (labelMat - h)
        weights += alpha* (dataMatrix.transpose())*error  #梯度
    return weights

def stocGradAscent0(dataMatrix, classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix*weights))
        error = classLabels[i]-h
        weights += alpha * error * dataMatrix[i]
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.01
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex]-h
            weights += alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def plotBestFit(wei):
    import matplotlib.pyplot as plt
    weights = wei
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord0 = []; ycord0=[]
    xcord1 = []; ycord1=[]
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord0.append(dataArr[i,1]); ycord0.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1, s=30, c='red', marker = 's')
    ax.scatter(xcord0,ycord0, s=30, c='green')
    x = arange(-3.0,3.0,0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('x1');plt.ylabel('x2')
    plt.show()

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob>0.5:return 1.0
    else: return 0.0

def colicTest():
    frTrain = open(r'/Users/lyj/Programs/Codes&Data/machinelearninginaction/Ch05/horseColicTraining.txt')
    frTest = open(r'/Users/lyj/Programs/Codes&Data/machinelearninginaction/Ch05/horseColicTest.txt')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet),trainingLabels,500)
    errorCount = 0.0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec +=1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr),trainWeights)) != int(currLine[21]):
            errorCount += 1.0
    errorRate = (errorCount/numTestVec)
    print "The error rate of this test is: %f" % errorRate
    return errorRate

def multiTest():
    numTests = 10
    errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest()
    print "After %d iterations the average error rate is: %f" % (numTests,errorSum/numTests)

# dataArr, labelMat = loadDataSet()
# weight = gradAscent(dataArr, labelMat)
# weight0 = stocGradAscent0(array(dataArr), labelMat)
# weights = stocGradAscent1(array(dataArr), labelMat)
# plotBestFit(weight)
# plotBestFit(weights)

if __name__=='__main__':
    multiTest()