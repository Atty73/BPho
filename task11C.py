import matplotlib.pyplot as plt
import numpy as np

RED_FREQUENCY = 400
ORANGE_FREQUENCY = 480
YELLOW_FREQUENCY = 510
GREEN_FREQUENCY = 550
CYAN_FREQUENCY = 600
BLUE_FREQUENCY = 620
VIOLET_FREQUENCY = 750

SCATTER_SIZE = 3

def refIndexWater(freq):
    freqHz = freq * 10**12
    RHS = 1.731 - 0.261*((freqHz/(10**15))**2)
    n = np.sqrt(1 + np.sqrt(1/RHS))
    return n

def calcThetas(n):
    primaryTheta = np.rad2deg(np.arcsin(np.sqrt((4 - n ** 2) / 3)))
    secondaryTheta = np.rad2deg(np.arcsin(np.sqrt((9-n**2)/8)))

    return primaryTheta, secondaryTheta

def initialiseMatplotlib():
    global ax
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.grid(True, alpha=0.6)
    ax.set_axisbelow(True)
    ax.set_xlim(405, 750)
    ax.set_ylim(39, 49)

def calcPhi(theta, n):
    phi = np.arcsin((np.sin(np.deg2rad(theta))) / n)
    return np.rad2deg(phi)

def calcCriticalAngle(n):
    critAngle = np.arcsin(1/n)
    return np.rad2deg(critAngle)

def createGraph():
    thetaArray = np.linspace(0, 90, 91)
    primaryPhiArray = np.array([])
    secondaryPhiArray = np.array([])
    criticalAngleArray = np.array([])
    frequencies = np.linspace(405, 750, 346)

    for frequency in frequencies:
        primaryTheta, secondaryTheta = calcThetas(refIndexWater(frequency))
        primaryPhiArray = np.append(primaryPhiArray, calcPhi(primaryTheta, refIndexWater(frequency)))
        secondaryPhiArray = np.append(secondaryPhiArray, calcPhi(secondaryTheta, refIndexWater(frequency)))
        criticalAngleArray = np.append(criticalAngleArray, calcCriticalAngle(refIndexWater(frequency)))


    ax.scatter(frequencies[0:75], primaryPhiArray[0:75], color='red', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[76:105], primaryPhiArray[76:105], color='orange', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[106:125], primaryPhiArray[106:125], color='yellow', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[126:195], primaryPhiArray[126:195], color='green', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[196:215], primaryPhiArray[196:215], color='cyan', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[216:265], primaryPhiArray[216:265], color='blue', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[266:345], primaryPhiArray[266:345], color='violet', marker='o', s=SCATTER_SIZE)

    ax.scatter(frequencies[0:75], secondaryPhiArray[0:75], color='red', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[76:105], secondaryPhiArray[76:105], color='orange', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[106:125], secondaryPhiArray[106:125], color='yellow', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[126:195], secondaryPhiArray[126:195], color='green', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[196:215], secondaryPhiArray[196:215], color='cyan', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[216:265], secondaryPhiArray[216:265], color='blue', marker='o', s=SCATTER_SIZE)
    ax.scatter(frequencies[266:345], secondaryPhiArray[266:345], color='violet', marker='o', s=SCATTER_SIZE)

    ax.plot(frequencies, primaryPhiArray, color='red', linewidth=1)
    ax.plot(frequencies, secondaryPhiArray, color='blue', linewidth=1)
    ax.plot(frequencies, criticalAngleArray, color='black')

def main():
    initialiseMatplotlib()
    createGraph()

    plt.show()

if __name__ == '__main__':
    main()
