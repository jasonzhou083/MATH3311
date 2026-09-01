from numpy import arange, sin, pi
import matplotlib.pyplot as plt

### BEGIN SOLUTION
def f(x):
    return sin(pi * x)

print('(a) f(k) = 0 for all k.')
x = arange(101)
y = f(x)
plt.plot(x, y, 'o')
plt.grid(True)
plt.xlabel('k')
### END SOLUTION