import matplotlib.pyplot as plt
import numpy as np
import functions as f
import math

c1 = 3*10**8
c2 = 10**8

def fermat(xArray):
    tArray = []
    for x in xArray:
        squareRoot1 = math.sqrt(x**2+y**2)
        squareRoot2 = math.sqrt((L-x)**2+y**2)
        t = (squareRoot1+squareRoot2)/(c/n)
        tArray.append(t)
    return tArray