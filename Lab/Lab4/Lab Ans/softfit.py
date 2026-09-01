# MATH3311/MATH5335: softfit.py
#

# Exercises 7, Question 4 solution

# Purpose

# Solve nonlinear equations for software productivity model
#
#   P = x_0 * L^x_1 * S^x_2
#
# Note that in all these models the variable x_2 < 0, indicating that
# software productivity DECREASES as staffing levels increases!

from scipy.optimize import root, least_squares
from scipy.linalg import lstsq
from numpy import empty, array, float64, log, exp

def softprod(x, L, S, P, jac=True):
    """Residual function for P = x_1 L^x_2 S^x_3.

    If jac is True, then returns residual r and Jacobian J.
    If jac is False, then returns only r."""
    r1 = L**x[1]
    r2 = S**x[2]
    r12 = r1 * r2
    rr = x[0] * r12
    r = rr - P
    if jac:
        J = empty((3, 3))
        J[:,0] = r12
        J[:,1] = rr * log(L)
        J[:,2] = rr * log(S)
        return r, J
    else:
        return r

def display_step(x, f):
    print(f'{x:20.15e}  {f:10.2e}')

# Problem data

P = array([450, 830, 547, 628, 1508], dtype=float64)
L = array([3539, 42487, 12620, 21698, 30521], dtype=float64)
S = array([3, 7, 5, 6, 4], dtype=float64)

# Starting point
x0 = array([5, 1, -1], dtype=float64)

# Solve systems of nonlinear equations

# Model has three variables, so choose three data values
# to be satisfied as equalities.

selections = [ [0,1,2], [0,2,3], [0,2,4], [1,2,3], [1,2,4], [2,3,4] ]
jac = True

print('Attempt to solve exactly by selecting subsets of three data values\n')
for I in selections:
    sol = root(softprod, x0, args=(L[I], S[I], P[I], jac), method='lm', jac=jac)
    print('Using variables', I)
    print('\tx = ', sol.x)
    print('\tresidual = ', sol.fun)

print('\nUse all data for nonlinear least squares\n')
result = least_squares(softprod, x0, args=(L, S, P, False))
print('\t', result.message)
if result.success:
    print('\tx = ', result.x)
    print('\tresidual = ', result.fun)

print('\nConvert to a linear problem by taking logs\n')
# Taking logs of the model P = x_0 * L^x_1 * S^x_2 gives
# log(P) = log(x_0) + x_1 * log(L) + x_2 * log(S)
# which is linear in the variables log(x_0), x_1 and x_2.
print('\nLinear model: log(P) = log(x_0) + x_1 * log(L) + x_2 * log(S)\n')
A = empty((len(L), 3))
A[:,0] = 1.0
A[:,1] = log(L)
A[:,2] = log(S)
xlin, residues, rank, s = lstsq(A, log(P))
xlin[0] = exp(xlin[0])
print('\tx = ', xlin)
print('\t||residual||^2 = ', residues)