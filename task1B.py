import matplotlib.pyplot as plt
import numpy as np
import functions as f
import math

#Function for calculating refractive index
def refIndexWater(freq):
    freqHz = freq * 10**12
    RHS = 1.731 - 0.261*((freqHz/(10**15))**2)
    n = math.sqrt(1 + math.sqrt(1/RHS))
    print(n)
    return n

#Defining array of frequencies
frequencies = f.linspace(405, 791, 1544)
print(frequencies)
#nValues = []

for i in range(len(frequencies)):
    colour = (0,0,0)
    if frequencies[i] <= 482:
        x = frequencies[i]-405
        y = x/77
        colour = (1, y, 0)
    elif frequencies[i] >= 482 and frequencies[i] <= 559:
        x = frequencies[i]-482
        y = 1-(x/77)
        colour = (y, 1, 0)
    elif frequencies[i] >= 559 and frequencies[i] <= 636:
        x = frequencies[i]-559
        y = x/77
        colour = (0, 1, y)
    elif frequencies[i] >= 636 and frequencies[i] <= 713:
        x = frequencies[i]-636
        y = 1-(x/77)
        colour = (0, y, 1)
    elif frequencies[i] >= 713 and frequencies[i] <= 790:
        x = frequencies[i]-713
        y = x/77
        colour = (y, 0, 1)

    plt.plot(frequencies[i], refIndexWater(frequencies[i]), marker='o', color=colour, markersize=1)

#Calculating index for each frequency
#for frequency in frequencies:
    #nValues.append(refIndexWater(frequency))

#plt.plot(frequencies, nValues,'b-o',ms=1)

plt.xlabel("Frequency / THz")
plt.ylabel("n")
plt.title("Refractive index of water over visible range")

plt.show()