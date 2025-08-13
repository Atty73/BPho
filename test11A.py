import matplotlib.pyplot as plt
import numpy as np

RED_FREQUENCY = 400
ORANGE_FREQUENCY = 480
YELLOW_FREQUENCY = 510
GREEN_FREQUENCY = 550
CYAN_FREQUENCY = 600
BLUE_FREQUENCY = 620
VIOLET_FREQUENCY = 750


# Corrected function for primary rainbow: epsilon = 4*arcsin(...) - 2*theta
def calcPrimaryEpsilon(theta, n):
    theta_radians = np.deg2rad(theta)
    inverse = np.sin(theta_radians) / n
    # Make sure arcsin argument is within [-1, 1]
    if np.abs(inverse) > 1:
        return np.nan
    epsilon = 4 * np.arcsin(inverse) - 2 * theta_radians
    return np.rad2deg(epsilon)


# Corrected function for secondary rainbow: epsilon = pi - 6*arcsin(...) + 2*theta
def calcSecondaryEpsilon(theta, n):
    theta_radians = np.deg2rad(theta)
    inverse = np.sin(theta_radians) / n
    # Make sure arcsin argument is within [-1, 1]
    if np.abs(inverse) > 1:
        return np.nan
    epsilon = np.pi - 6 * np.arcsin(inverse) + 2 * theta_radians
    return np.rad2deg(epsilon)


def refIndexWater(freq):
    freqHz = freq * 10 ** 12
    # Ensure denominator is not zero or negative
    rhs_denominator = 1.731 - 0.261 * ((freqHz / (10 ** 15)) ** 2)
    if rhs_denominator <= 0:
        return np.nan
    rhs = 1 / rhs_denominator
    # Ensure inner part of sqrt is not negative
    if 1 + np.sqrt(rhs) < 0:
        return np.nan
    n = np.sqrt(1 + np.sqrt(rhs))
    return n


# Corrected minEpsilons to use the correct formulas for theta
def minEpsilons(n):
    # Formulas for theta are based on the derivative of the epsilon equations.
    # The primary rainbow's minimum deviation angle corresponds to the formula with sqrt((4-n**2)/3)
    # The secondary rainbow's minimum deviation angle corresponds to the formula with sqrt((9-n**2)/8)

    # Check for valid arguments for arcsin
    primary_arg = (4 - n ** 2) / 3
    if primary_arg < 0:
        primaryTheta = np.nan
    else:
        primaryTheta = np.arcsin(np.sqrt(primary_arg))

    secondary_arg = (9 - n ** 2) / 8
    if secondary_arg < 0:
        secondaryTheta = np.nan
    else:
        secondaryTheta = np.arcsin(np.sqrt(secondary_arg))

    # Convert theta to degrees for the calc functions
    primary_epsilon = calcPrimaryEpsilon(np.rad2deg(primaryTheta), n)
    secondary_epsilon = calcSecondaryEpsilon(np.rad2deg(secondaryTheta), n)

    # Return two arrays of the constant epsilon values for plotting
    theta_array_for_lines = np.linspace(0, 90, 91)
    return np.full_like(theta_array_for_lines, primary_epsilon), np.full_like(theta_array_for_lines, secondary_epsilon)


def initialiseMatplotlib():
    global ax
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.grid(True, alpha=0.6)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 180)
    plt.title('Elevation of Deflected Beam /deg')
    plt.xlabel('$\\theta$ /deg')
    plt.ylabel('$\\epsilon$ /deg')


def createGraph():
    thetaArray = np.linspace(0, 90, 91)

    # Refactor to use a dictionary for better organization and less repetition
    colors = {
        'red': RED_FREQUENCY, 'orange': ORANGE_FREQUENCY, 'yellow': YELLOW_FREQUENCY,
        'green': GREEN_FREQUENCY, 'cyan': CYAN_FREQUENCY, 'blue': BLUE_FREQUENCY,
        'violet': VIOLET_FREQUENCY
    }

    for color_name, freq in colors.items():
        n = refIndexWater(freq)

        # Calculate epsilon arrays for the curves
        primary_epsilon_curve = np.array([calcPrimaryEpsilon(theta, n) for theta in thetaArray])
        secondary_epsilon_curve = np.array([calcSecondaryEpsilon(theta, n) for theta in thetaArray])

        # Calculate the straight lines for the minimum deviation angles
        primary_min_line, secondary_min_line = minEpsilons(n)

        # Plot the curves
        ax.plot(thetaArray, primary_epsilon_curve, color=color_name)
        ax.plot(thetaArray, secondary_epsilon_curve, color=color_name)

        # Plot the straight lines
        ax.plot(thetaArray, primary_min_line, color=color_name)
        ax.plot(thetaArray, secondary_min_line, color=color_name)


def main():
    initialiseMatplotlib()
    createGraph()
    plt.show()


if __name__ == '__main__':
    main()