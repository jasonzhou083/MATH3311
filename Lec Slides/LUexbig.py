from numpy.random import rand, randn
from numpy import eye, inf
from scipy.linalg import lu_factor, lu_solve, inv, solve, norm
from time import time

n = 2000
print(f'Solving an nxn linear system Ax=b with n = {n}:')

# Matrix with elements uniformly distributed in [0,1].
R = rand(n, n) 

# Add 1 along the main diagonal.
A = eye(n) + R

# RHS vectors
b1 = rand(n)  # uniform random elements
b2 = randn(n) # normal random elements

# Solve using LU factorisation.
start = time()
lu, piv = lu_factor(A)
x1 = lu_solve((lu, piv), b1)
finish = time()
print(f'  * lu_factor and lu_solve took {finish-start:0.4f} secs,', end='')
r1 = norm(b1 - A@x1, inf)
print(f' (residual = {r1:0.3e})')

# Solve using inverse.
start = time()
A_inv = inv(A)
x1 = A_inv @ b1
finish = time()
print(f'  * inv(A) took {finish-start:0.4f} secs,', end='')
r1 = norm(b1 - A@x1, inf)
print(f' (residual = {r1:0.3e})')

# Two right-hand sides
print(f'\nSolving for two different right-hand sides:')
start = time()
x1 = solve(A, b1)
x2 = solve(A, b2)
finish = time()
print(f'  * solve took {finish-start:0.4f} secs,', end='')
r1 = norm(b1 - A@x1, inf)
r2 = norm(b2 - A@x2, inf)
print(f' (residuals = {r1:0.3e}, {r2:0.3e})')

# Two right-hand sides with only one LU factorisation.
start = time()
lu, piv = lu_factor(A)
x1 = lu_solve((lu, piv), b1)
x2 = lu_solve((lu, piv), b2)
finish = time()
print(f'  * lu_factor and lu_solve took {finish-start:0.4f} secs,', end='')
r1 = norm(b1 - A@x1, inf)
r2 = norm(b2 - A@x2, inf)
print(f' (residuals = {r1:0.3e}, {r2:0.3e})')
