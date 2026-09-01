# MATH3311/MATH5335: ex07q2sol.m
# Exercises 7, Question 2 solution

from numpy import exp, linspace, inf
from scipy.linalg import norm
from blackscholes import bsput
import matplotlib.pyplot as plt

# Purpose: calculate the implied volatility for a European put option.
#
# Put = right to sell the asset for agreed price K at expiry
# so boundary condition at expiry is max(K-S, 0)

# Problem data

# Example data from Lectures with higher strike     
Tmt  = 0.5    # time to maturity in years
r    = 0.053  # risk-free interest rate per year
S    = 32.75  # current stock price

# Strike for out of the money put
#K    = 32.00
# Strike for in the money put
K    = 35.00

# Limit as volatility goes to 0

# As volatility sigma goes to 0 from above,
# limit depends on whether put is
#  in the money     S < K*exp(-r*Tmt)
#  out of the money S > K*exp(-T*Tmt)
Kpv = K*exp(-r*Tmt)
print(f'S = {S:0.2f}, K*exp(-r*(T-t)) = {Kpv:0.2f}\n')

# Limiting value as sigma goes to 0 from above
p0 = max(Kpv - S, 0)

# Plot put value and its derivative w.r.t. volatility

# Vector of values of sigma
# Is this a fine enough grid to get a smooth curve close to zero?
SIG = linspace(0, 1, 501)
# Increasing the number of grid points by a factor of 10
# decreases the finite difference width h by a factor of 10
# which should reduce the finite difference error by 100
# as central difference approximation to first derivative is O(h^2)
#SIG = linspace(0, 1, 5001)

# Calculate vector of put option values and derivatives
PUT, DPDS = bsput(S, K, r, SIG, Tmt)

# Finite difference check of derivatives
h = SIG[1]-SIG[0]
FD = ( PUT[2:] - PUT[:-2] ) / (2*h)
FDchk = norm(DPDS[1:-1]-FD, inf)
print(f'FDchk = {FDchk:0.2e}')

# Plot put values
plt.figure(1, figsize=(7.0, 4.8))
plt.subplot(2, 1, 1)
plt.plot(SIG, PUT, [0, 1], [p0, p0], 'r--')
plt.grid(True)
plt.xlabel('Volatility $\sigma$')
str = 'Black-Scholes put value as a function of $\sigma$: '
plt.title(str+f' S = {S:0.2f}, K exp(-r(T-t)) = {Kpv:0.2f}')
plt.subplot(2, 1, 2)
plt.plot(SIG, DPDS, SIG[1:-1], FD)
plt.legend(('Calculated derivative $p''(\sigma)$',
            'Central difference approximation'))
plt.grid(True)
plt.title('Derivative of put w.r.t. volatility $\sigma$')
plt.xlabel('Volatility $\sigma$')
plt.tight_layout(pad=1.0)
           