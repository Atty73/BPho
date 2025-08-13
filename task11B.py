import matplotlib.pyplot as plt
import numpy as np

RED_FREQUENCY = 400
ORANGE_FREQUENCY = 480
YELLOW_FREQUENCY = 510
GREEN_FREQUENCY = 550
CYAN_FREQUENCY = 600
BLUE_FREQUENCY = 620
VIOLET_FREQUENCY = 750


def calcPrimaryEpsilon(theta, n):
    theta_radians = np.deg2rad(theta)
    inverse = np.sin(theta_radians)/n
    epsilon = 4*np.arcsin(inverse) - 2*theta_radians
    return np.rad2deg(epsilon)

def refIndexWater(freq):
    freqHz = freq * 10**12
    RHS = 1.731 - 0.261*((freqHz/(10**15))**2)
    n = np.sqrt(1 + np.sqrt(1/RHS))
    return n

def calcSecondaryEpsilon(theta, n):
    theta_radians = np.deg2rad(theta)
    inverse = np.sin(theta_radians) / n
    epsilon = np.pi - 6 * np.arcsin(inverse) + 2 * theta_radians
    return np.rad2deg(epsilon)

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
    ax.set_ylim(40, 54)

def createGraph():
    thetaArray = np.linspace(0, 90, 91)
    primaryEpsilonArray = np.array([])
    secondaryEpsilonArray = np.array([])
    frequencies = np.linspace(405, 750, 346)

    for frequency in frequencies:
        primaryTheta, secondaryTheta = calcThetas(refIndexWater(frequency))
        primaryEpsilonArray = np.append(primaryEpsilonArray, calcPrimaryEpsilon(primaryTheta, refIndexWater(frequency)))
        secondaryEpsilonArray = np.append(secondaryEpsilonArray, calcSecondaryEpsilon(secondaryTheta, refIndexWater(frequency)))

    ax.scatter(frequencies[0:75], primaryEpsilonArray[0:75], color='red', marker='o', s=3)
    ax.scatter(frequencies[76:105], primaryEpsilonArray[76:105], color='orange', marker='o', s=3)
    ax.scatter(frequencies[106:125], primaryEpsilonArray[106:125], color='yellow', marker='o', s=3)
    ax.scatter(frequencies[126:195], primaryEpsilonArray[126:195], color='green', marker='o', s=3)
    ax.scatter(frequencies[196:215], primaryEpsilonArray[196:215], color='cyan', marker='o', s=3)
    ax.scatter(frequencies[216:265], primaryEpsilonArray[216:265], color='blue', marker='o', s=3)
    ax.scatter(frequencies[266:345], primaryEpsilonArray[266:345], color='violet', marker='o', s=3)

    ax.scatter(frequencies[0:75], secondaryEpsilonArray[0:75], color='red', marker='o', s=3)
    ax.scatter(frequencies[76:105], secondaryEpsilonArray[76:105], color='orange', marker='o', s=3)
    ax.scatter(frequencies[106:125], secondaryEpsilonArray[106:125], color='yellow', marker='o', s=3)
    ax.scatter(frequencies[126:195], secondaryEpsilonArray[126:195], color='green', marker='o', s=3)
    ax.scatter(frequencies[196:215], secondaryEpsilonArray[196:215], color='cyan', marker='o', s=3)
    ax.scatter(frequencies[216:265], secondaryEpsilonArray[216:265], color='blue', marker='o', s=3)
    ax.scatter(frequencies[266:345], secondaryEpsilonArray[266:345], color='violet', marker='o', s=3)

def main():
    initialiseMatplotlib()
    createGraph()

    plt.show()

if __name__ == '__main__':
    main()
