import matplotlib.pyplot as plt
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

plt.plot(xArray, tArray, color='blue', linewidth=2)
plt.scatter(1,tArray[len(tArray)//2], marker='*', color='red',zorder=2)
plt.xlabel("x / m")
plt.ylabel("t / s")
plt.text(1,1.06e-8,f"L = {L}m")
plt.grid(True)
plt.show()