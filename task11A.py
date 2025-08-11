import matplotlib.pyplot as plt
import numpy as np

def calcTheta(n):
    root = np.sqrt((9-n**2)/8)
    theta = np.arcsin(root)
    return theta

def calcEpsilon(theta, n):
     inverse = np.sin(theta)/n
     epsilon = np.pi - 6*np.arcsin(inverse) + 2*theta
     return epsilon

