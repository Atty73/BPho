import matplotlib.pyplot as plt
import numpy as np

#Percentage difference function
def percentageDifference(experimental, actual):
    pd = abs(((experimental - actual) / actual) * 100)
    return pd

#Defining indices for values of U and V in lensArray
U_INDEX = 0
V_INDEX = 1

lensArray = [[20, 65.5], [25, 40], [30, 31], [35, 27], [40, 25], [45, 23.1], [50, 21.5], [55, 20.5]]

#Initialising 2 empty arrays to store 1/u and 1/v
recipUArray = np.zeros(8, dtype=float)
recipVArray = np.zeros(8, dtype=float)

#Filling arrays with 1/u and 1/v
for i in range(len(lensArray)):
    recipUArray[i] = 1 / lensArray[i][U_INDEX]
    recipVArray[i] = 1 / lensArray[i][V_INDEX]

#Using numpy to find a line of best fit
m, c = np.polyfit(recipUArray,recipVArray,1)

#Plotting line of best fit and experimental data points
plt.plot(recipUArray, m*recipUArray+c, 'b-o', ms=1)
plt.scatter(recipUArray, recipVArray, c="red", marker="+", s=30)
plt.xlabel("1/u")
plt.ylabel("1/v")
plt.title("Thin lens")
plt.text(0.028, 0.045, f"Gradient: {m} \nPercentage Difference: {percentageDifference(m, -1)}%")

plt.show()

