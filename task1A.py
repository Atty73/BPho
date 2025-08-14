import matplotlib.pyplot as plt
import functions as f
import math

#Function for Sellmeier's Equation
def Sellmeier(wavelength):
    wavelengthMicro = wavelength/1000

    #Sellmeier coefficients
    a = [1.03961212, 0.231792344, 1.01146945]
    b = [0.00600069867, 0.0200179144, 103.560653]
    sum = 0
    for k in range (0, 2):
        sum += (a[k]*(wavelengthMicro**2))/((wavelengthMicro**2)-b[k])
    n = math.sqrt(1+sum)
    return n

wavelengths = f.linspace(400, 800, 400)
nValues = []
for i in wavelengths:
    nValues.append(Sellmeier(i))

plt.plot(wavelengths, nValues,'r-o',ms=1)

plt.xlabel("Wavelength / nm")
plt.ylabel("n")
plt.title("Refractive Index of Crown Glass")

plt.show()