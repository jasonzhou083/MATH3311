# MATH3311/MATH5335: ex07q1sol.m
# Exercises 7, Question 1 solution

from numpy import linspace, array, float64, finfo, zeros_like, empty
from datetime import date
from blackscholes import blackscholes
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
    
# Recent NAB example
# Current asset price
S = 34.810
# Risk free interest rate
r = 0.025
# Vector of strikes
K = linspace(33.5, 36, 6)
# Corresponding vector of call prices
cmkt = array([1.460, 1.040, 0.640, 0.370, 0.155, 0.070])
# Dates: today and expiry
t0 = date.fromisoformat('2014-08-27')
tf = date.fromisoformat('2014-09-25')

# Convert to years using 365 day basis
# datenum converts dates to number of days from specific date in past
Tmt = (tf-t0).days / 365

# Solve for implied volatility

# Implied volatility should be in sigint = [siglo, sighi]
siglo = finfo(float64).eps
sighi = 1.0
sigint = [siglo, sighi]

# Vector of sigma values for plotting
SIG = linspace(0, sighi, 401)
f_values = empty((len(K), len(SIG)))

# Loop over all strikes and solve for implied volatility
IV = zeros_like(K)

def blackscholes_value(sigma, K):
    c, dcds = blackscholes(S, K, r, sigma, Tmt)
    return c

for j, Kj in enumerate(K):
    fj = lambda sigma: blackscholes_value(sigma, Kj) - cmkt[j]
    soln = root_scalar(fj, bracket=sigint, method='brentq')
    IV[j] = soln.root
    f_values[j,:] = fj(SIG)                 

# Use a plot to check calculation
plt.figure(1)
plt.plot(SIG, f_values.T, IV, zeros_like(IV), 'r*')
plt.axis((0.0, 0.4, -1.0, 1.0))
plt.grid(True)
plt.xlabel('$\sigma$')

# Plot implied volatility against strike

# In a Black-Scholes world the volatility should be constant, 
# so should not change with changing strike
plt.figure(2)
plt.plot(K, IV)
plt.grid(True)
plt.title('Implied volatility vs Strike')
plt.xlabel('Strike $K$')
