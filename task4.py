import matplotlib.pyplot as plt
import numpy as np
import functions as f
import math

#defining arbitrary values to use in formula
y = 1
Y = 2
L = 4
theta = 30

c = 3*10**8

c1 = float(input("Wavespeed 1: "))
c2 = float(input("Wavespeed 2: "))

n1 = c/c1
n2 = c/c2


def calcT(xArray):
    tArray = []
    for x in xArray:
        squareRoot1 = np.sqrt(Y**2+x**2)
        squareRoot2 = np.sqrt(y**2+(L-x)**2)
        t = squareRoot1/c1 + squareRoot2/c2
        tArray.append(t)
    return tArray

def findLowestValueIndex(array):
    lowestValueIndex = 0
    lowestValue = array[0]
    for i in range(len(array)):
        if array[i] < lowestValue:
            lowestValue = array[i]
            lowestValueIndex = i
    return lowestValueIndex

def calcTheta(x):
    theta = np.arctan(x/Y)
    return np.rad2deg(theta)

def calcPhi(x):
    phi = np.arctan((L-x)/y)
    return np.rad2deg(phi)

xArray = f.linspace(0,L,60000)
tArray = calcT(xArray)

lowestTIndex = findLowestValueIndex(tArray)
minimumX = xArray[lowestTIndex]
print(f"sin(theta)/c1 = {np.sin(np.deg2rad(calcTheta(minimumX))) / c1}")
print(f"sin(phi)/c2 = {np.sin(np.deg2rad(calcPhi(minimumX))) / c2}")

plt.plot(xArray, tArray, color='blue')
plt.scatter(minimumX, tArray[lowestTIndex], marker="*", color='red', zorder=3)
plt.grid(True)
plt.xlabel("x / m")
plt.ylabel("t / s")
plt.show()