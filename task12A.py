import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from matplotlib.patches import Rectangle

triangleX = [15,25,35,15]
triangleY = [20,45,20,20]

def createIncidenceNormal(x, y):
    gradient = -1/((y[1]-y[0])/(x[1]-x[0]))
    normalX = []
    normalY = []
    for i in range(x[0],x[1]):
        normalX.append(i)
        normalY.append(40+i*gradient)
    ax.plot(normalX, normalY, color='white', ls = 'dashed')
    print(normalY, x[1]-1)
    return normalX, normalY

def createTriangle(x, y):
    ax.plot(triangleX, triangleY, color='white')

def createBackground():
    background = Rectangle(xy=(0, 0), width=256, height=256, color='black')
    ax.add_patch(background)

def initialiseMatplotlib():
    global ax
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    plt.axis('off')

def createIncidentRay(thetaI, normalX, normalY):
    incX = [normalX[0], normalX[-1]]
    y1 = (abs(normalX[-1]-normalX[0])*np.tan(np.radians(90) - np.radians(thetaI) - np.arctan(abs((normalX[-1]-normalX[0])/normalY[0]-normalY[-1]))) + normalY[-1])
    incY = [y1, normalY[-1]]
    plt.plot(incX, incY, color='white')


def main():
    initialiseMatplotlib()
    normalX, normalY = createIncidenceNormal(triangleX, triangleY)
    createIncidentRay(90, normalX, normalY)
    createTriangle(triangleX, triangleY)
    createBackground()

    plt.show()

if __name__ == '__main__':
    main()