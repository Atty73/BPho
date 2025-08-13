import matplotlib.pyplot as plt
import numpy as np

RED_FREQUENCY = 400
ORANGE_FREQUENCY = 480
YELLOW_FREQUENCY = 510
GREEN_FREQUENCY = 550
CYAN_FREQUENCY = 600
BLUE_FREQUENCY = 620
VIOLET_FREQUENCY = 750


def calcSecondaryEpsilon(theta, n):
     theta_radians = np.deg2rad(theta)
     inverse = np.sin(theta_radians)/n
     epsilon = np.pi - 6*np.arcsin(inverse) + 2*theta_radians
     return np.rad2deg(epsilon)

def refIndexWater(freq):
    freqHz = freq * 10**12
    RHS = 1.731 - 0.261*((freqHz/(10**15))**2)
    n = np.sqrt(1 + np.sqrt(1/RHS))
    return n

def calcPrimaryEpsilon(theta, n):
    theta_radians = np.deg2rad(theta)
    inverse = np.sin(theta_radians)/n
    epsilon = 4*np.arcsin(inverse) - 2*theta_radians
    return np.rad2deg(epsilon)

def minEpsilons(n):
    primaryTheta = np.rad2deg(np.arcsin(np.sqrt((4-n**2)/3)))
    secondaryTheta = np.rad2deg(np.arcsin(np.sqrt((9-n**2)/8)))

    primaryEpsilon = calcPrimaryEpsilon(primaryTheta, n)
    secondaryEpsilon = calcSecondaryEpsilon(secondaryTheta, n)

    return np.array([primaryEpsilon]*91), np.array([secondaryEpsilon]*91)

def initialiseMatplotlib():
    global ax
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.grid(True, alpha=0.6)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 180)

def createGraph():
    thetaArray = np.linspace(0, 90, 91)
    redPrimaryEpsilonArray = np.array([])
    orangePrimaryEpsilonArray = np.array([])
    yellowPrimaryEpsilonArray = np.array([])
    greenPrimaryEpsilonArray = np.array([])
    cyanPrimaryEpsilonArray = np.array([])
    bluePrimaryEpsilonArray = np.array([])
    violetPrimaryEpsilonArray = np.array([])

    redSecondaryEpsilonArray = np.array([])
    orangeSecondaryEpsilonArray = np.array([])
    yellowSecondaryEpsilonArray = np.array([])
    greenSecondaryEpsilonArray = np.array([])
    cyanSecondaryEpsilonArray = np.array([])
    blueSecondaryEpsilonArray = np.array([])
    violetSecondaryEpsilonArray = np.array([])

    for theta in thetaArray:
        redPrimaryEpsilonArray = np.append(redPrimaryEpsilonArray, calcPrimaryEpsilon(theta, refIndexWater(RED_FREQUENCY)), axis=None)
        redSecondaryEpsilonArray = np.append(redSecondaryEpsilonArray, calcSecondaryEpsilon(theta, refIndexWater(RED_FREQUENCY)), axis=None)
        redMinimumPrimaryEpsilon, redMinimumSecondaryEpsilon = minEpsilons(refIndexWater(RED_FREQUENCY))

        orangePrimaryEpsilonArray = np.append(orangePrimaryEpsilonArray,calcPrimaryEpsilon(theta, refIndexWater(ORANGE_FREQUENCY)), axis=None)
        orangeSecondaryEpsilonArray = np.append(orangeSecondaryEpsilonArray,calcSecondaryEpsilon(theta, refIndexWater(ORANGE_FREQUENCY)), axis=None)
        orangeMinimumPrimaryEpsilon, orangeMinimumSecondaryEpsilon = minEpsilons(refIndexWater(ORANGE_FREQUENCY))

        yellowPrimaryEpsilonArray = np.append(yellowPrimaryEpsilonArray,calcPrimaryEpsilon(theta, refIndexWater(YELLOW_FREQUENCY)), axis=None)
        yellowSecondaryEpsilonArray = np.append(yellowSecondaryEpsilonArray,calcSecondaryEpsilon(theta, refIndexWater(YELLOW_FREQUENCY)), axis=None)
        yellowMinimumPrimaryEpsilon, yellowMinimumSecondaryEpsilon = minEpsilons(refIndexWater(YELLOW_FREQUENCY))

        greenPrimaryEpsilonArray = np.append(greenPrimaryEpsilonArray,calcPrimaryEpsilon(theta, refIndexWater(GREEN_FREQUENCY)), axis=None)
        greenSecondaryEpsilonArray = np.append(greenSecondaryEpsilonArray,calcSecondaryEpsilon(theta, refIndexWater(GREEN_FREQUENCY)), axis=None)
        greenMinimumPrimaryEpsilon, greenMinimumSecondaryEpsilon = minEpsilons(refIndexWater(GREEN_FREQUENCY))

        cyanPrimaryEpsilonArray = np.append(cyanPrimaryEpsilonArray,calcPrimaryEpsilon(theta, refIndexWater(CYAN_FREQUENCY)), axis=None)
        cyanSecondaryEpsilonArray = np.append(cyanSecondaryEpsilonArray,calcSecondaryEpsilon(theta, refIndexWater(CYAN_FREQUENCY)), axis=None)
        cyanMinimumPrimaryEpsilon, cyanMinimumSecondaryEpsilon = minEpsilons(refIndexWater(CYAN_FREQUENCY))

        bluePrimaryEpsilonArray = np.append(bluePrimaryEpsilonArray,calcPrimaryEpsilon(theta, refIndexWater(BLUE_FREQUENCY)), axis=None)
        blueSecondaryEpsilonArray = np.append(blueSecondaryEpsilonArray,calcSecondaryEpsilon(theta, refIndexWater(BLUE_FREQUENCY)), axis=None)
        blueMinimumPrimaryEpsilon, blueMinimumSecondaryEpsilon = minEpsilons(refIndexWater(BLUE_FREQUENCY))

        violetPrimaryEpsilonArray = np.append(violetPrimaryEpsilonArray,calcPrimaryEpsilon(theta, refIndexWater(VIOLET_FREQUENCY)), axis=None)
        violetSecondaryEpsilonArray = np.append(violetSecondaryEpsilonArray, calcSecondaryEpsilon(theta, refIndexWater(VIOLET_FREQUENCY)), axis=None)
        violetMinimumPrimaryEpsilon, violetMinimumSecondaryEpsilon = minEpsilons(refIndexWater(VIOLET_FREQUENCY))

    ax.plot(thetaArray, redPrimaryEpsilonArray, color='red')
    ax.plot(thetaArray, redSecondaryEpsilonArray, color='red')
    ax.plot(thetaArray, redMinimumPrimaryEpsilon, color='red')
    ax.plot(thetaArray, redMinimumSecondaryEpsilon, color='red')

    ax.plot(thetaArray, orangePrimaryEpsilonArray, color='orange')
    ax.plot(thetaArray, orangeSecondaryEpsilonArray, color='orange')
    ax.plot(thetaArray, orangeMinimumPrimaryEpsilon, color='orange')
    ax.plot(thetaArray, orangeMinimumSecondaryEpsilon, color='orange')

    ax.plot(thetaArray, yellowPrimaryEpsilonArray, color='yellow')
    ax.plot(thetaArray, yellowPrimaryEpsilonArray, color='yellow')
    ax.plot(thetaArray, yellowMinimumPrimaryEpsilon, color='yellow')
    ax.plot(thetaArray, yellowMinimumSecondaryEpsilon, color='yellow')

    ax.plot(thetaArray, greenPrimaryEpsilonArray, color='green')
    ax.plot(thetaArray, greenSecondaryEpsilonArray, color='green')
    ax.plot(thetaArray, greenMinimumPrimaryEpsilon, color='green')
    ax.plot(thetaArray, greenMinimumSecondaryEpsilon, color='green')

    ax.plot(thetaArray, cyanPrimaryEpsilonArray, color='cyan')
    ax.plot(thetaArray, cyanSecondaryEpsilonArray, color='cyan')
    ax.plot(thetaArray, cyanMinimumPrimaryEpsilon, color='cyan')
    ax.plot(thetaArray, cyanMinimumSecondaryEpsilon, color='cyan')

    ax.plot(thetaArray, bluePrimaryEpsilonArray, color='blue')
    ax.plot(thetaArray, blueSecondaryEpsilonArray, color='blue')
    ax.plot(thetaArray, blueMinimumPrimaryEpsilon, color='blue')
    ax.plot(thetaArray, blueMinimumSecondaryEpsilon, color='blue')

    ax.plot(thetaArray, violetPrimaryEpsilonArray, color='violet')
    ax.plot(thetaArray, violetSecondaryEpsilonArray, color='violet')
    ax.plot(thetaArray, violetMinimumPrimaryEpsilon, color='violet')
    ax.plot(thetaArray, violetMinimumSecondaryEpsilon, color='violet')

def main():
    initialiseMatplotlib()
    createGraph()

    plt.show()

if __name__ == '__main__':
    main()
