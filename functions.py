import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

def linspace(min, max, noDataPoints):
    array = np.array([0]*noDataPoints,dtype="f")
    dataRange = max-min
    increment = dataRange/noDataPoints
    array[0] = min
    for i in range(1,noDataPoints):
        array[i] = array[i-1] + increment
    return array

def intLinspace(min, max, noDataPoints):
    array = np.array([0]*noDataPoints,dtype="i")
    dataRange = max-min
    increment = dataRange//noDataPoints
    array[0] = min
    for i in range(1,noDataPoints):
        array[i] = array[i-1] + increment
    return array


def linGradMaxY(minX, maxX, maxY, gradient):
    arrayX= np.array([minX,maxX],dtype="f")
    arrayY = np.array([0,maxY], dtype="f")
    minY = maxY-(gradient*(maxX-minX))
    arrayY[0] = minY
    return arrayX, arrayY


def linGradMinY(minX, maxX, minY, gradient):
    arrayX= np.array([minX,maxX],dtype="f")
    arrayY = np.array([minY,0],dtype="f")
    maxY = minY+(gradient*(maxX-minX))
    arrayY[1] = maxY
    return arrayX, arrayY

def linGradMidY(minX, maxX, midY, gradient):
    arrayX= np.array([minX,maxX],dtype="f")
    arrayY = np.array([0,0],dtype="f")
    midX = (maxX+minX)/2.0
    maxY = midY+(gradient*(maxX-midX))
    minY = midY-(gradient*(midX-minX))
    arrayY[0], arrayY[1] = minY, maxY
    return arrayX, arrayY

def findMid(a,b):
    mid = (a+b)/2
    return mid

def getFromExcel(filename, sheet, xColumn, yColumn):
    data = pd.read_excel(filename, sheet_name=sheet)
    x = data.iloc[:,xColumn].to_numpy()
    y = data.iloc[:,yColumn].to_numpy()
    return x, y

def theoGradient(x, y, gradient):
    lastValue = len(x)-1
    theoX, theoY = linGradMinY(x[0], x[lastValue], y[0], gradient)
    return theoX, theoY

def findLargest(a, b, c):
    if a>=b and a>=c:
        largest = a
    elif b>=a and b>=c:
        largest = b
    elif c>=a and c>=b:
        largest = c
    return largest

def findSmallest(a, b, c):
    if a<=b and a<=c:
        smallest = a
    elif b<=a and b<=c:
        smallest = b
    elif c<=a and c<=b:
        smallest = c
    return smallest

def plotUncertainty(filename, sheet, col1, col2, col3, xValues):
    data = pd.read_excel(filename, sheet_name=sheet)
    col1 = data.iloc[:,col1].to_numpy()
    col2 = data.iloc[:,col2].to_numpy()
    col3 = data.iloc[:,col3].to_numpy()
    for i in range(len(col1)):
        largest = findLargest(col1[i], col2[i], col3[i])
        smallest = findSmallest(col1[i], col2[i], col3[i])
        yValues = np.array([smallest,largest], dtype="f")
        xValues1 = np.array([xValues[i]]*2, dtype="f")
        plt.plot(xValues1, yValues, c="black", marker="_")


def findMean(filename, sheet, col1, col2, col3):
    data = pd.read_excel(filename, sheet_name=sheet)
    col1 = data.iloc[:,col1].to_numpy()
    col2 = data.iloc[:,col2].to_numpy()
    col3 = data.iloc[:,col3].to_numpy()
    print(col1,col2,col3)
    length = len(col1)
    yArray = np.array([0]*length, dtype="f")
    yArray[0] = col1[0]
    print(yArray)
    for i in range(len(col1)):
        yArray[i] = (col1[i]+col2[i]+col3[i])/3
        print((col1[i]+col2[i]+col3[i])/3)
    return yArray


def plotUncertaintyGradients(filename, sheet, col1, col2, col3, xValues):
    data = pd.read_excel(filename, sheet_name=sheet)
    col1 = data.iloc[:, col1].to_numpy()
    col2 = data.iloc[:, col2].to_numpy()
    col3 = data.iloc[:, col3].to_numpy()
    for i in range(len(col1)):
        largest = findLargest(col1[i], col2[i], col3[i])
        smallest = findSmallest(col1[i], col2[i], col3[i])
        yValues = np.array([smallest, largest], dtype="f")
        xValues1 = np.array([xValues[i]] * 2, dtype="f")
        plt.plot(xValues1, yValues, c="black", marker="_")
        if i == 0:
            leftLowest = smallest
            leftHighest = largest
        elif i == (len(col1)-1):
            rightHighest = largest
            rightLowest = smallest

    steepest = np.array([leftLowest, rightHighest], dtype="f")
    shallowest = np.array([leftHighest, rightLowest], dtype="f")
    firstAndLastX = np.array([xValues[0], xValues[-1]], dtype="f")

    plt.plot(firstAndLastX, steepest, c="yellow", marker="o", label="Steepest gradient")
    plt.plot(firstAndLastX, shallowest, c="pink", marker="o", label="Shallowest gradient")