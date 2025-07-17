import math

freq = 30000

RHS = 1.731 - 0.261*((freq/(10**15))**2)
n = math.sqrt((2*RHS+math.sqrt(4*RHS**2-4*RHS*(RHS-1)))/(2*RHS))
print(n)