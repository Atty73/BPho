import matplotlib.pyplot as plt
import numpy as np
import functions as f
import math

y = 1
n = 1
L = 2
c = 3*10**8
#x, t vary

def fermat(xArray):
    tArray = []
    for x in xArray:
        squareRoot1 = math.sqrt(x**2+y**2)
        squareRoot2 = math.sqrt((L-x)**2+y**2)
        t = (squareRoot1+squareRoot2)/(c/n)
        tArray.append(t)
    return tArray

xArray = f.linspace(0,2,600)
tArray = fermat(xArray)

plt.plot(xArray, tArray, color='red', linewidth=2)
plt.show()