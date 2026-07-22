from numpy import maximum, finfo, all, flip, arange, count_nonzero, min, max
from numpy import floor, log10, prod, diag, eye
from numpy.linalg import cond, eig
from scipy.linalg import cholesky, det, inv, LinAlgError
from matplotlib.pyplot import  semilogy, title, grid
from mat2npy import K

#from numpy import tril, triu
#from scipy.linalg import eigvalsh
#from scipy.io import loadmat
#from numpy.random import rand
#from scipy.linalg import solve_triangular
#d = loadmat('corr.mat')
#K = d['K']

# Part (a)
m, n = K.shape
print(f'(a) K is {m} x {n}, and is therefore square.')

# Part (b)
M =  maximum(abs(K), abs(K.T))
eps = finfo(float).eps
if all( abs(K - K.T) <= eps * M ):
    print('(b) K is symmetric')
else:
    print('(b) K is not symmetric')

# Part (c)    
try:
    R = cholesky(K)
except LinAlgError:
    print('(c) K is not positive definite')
else:
    print('(c) K is positive definite')

#Part (d) 
    
#w = eigvalsh(K)
w,v = eig(K)
w.sort()
w = flip(w)
semilogy(arange(1,n+1), w)
title('Eigenvalues of K')
grid(True)
print(f'(d) Smallest eigenvalue = {w.min()}, largest eigenvalue = {w.max()}')

# Part (e)

# i-
print(f'(e) scipy.linalg.det(K) = {det(K)}')
# ii- 
p = prod(diag(R))
print(f'\tCholesky factorization gives det(K) = {p**2}')
# iii-
p = prod(w)
print(f'\tEigenvalues give det(K) = {p}')

# Part (f) 

d = diag(K)
worst = max(abs(d-1))
print(f'(f) all diagonal elements of K equal 1 to within {worst:0.2e}')

# Part (g) Want minimum and maximum correlation between DIFFERENT assets

# i-
mincorr=min(K)

# ii- Correlation between an asset and itself = 1, so must avoid diagonal of K
# Subtract a HUGE number from diagonal elements so they cannot be maximum
 
maxcorr = max(K - 1e10*eye(n))

print(f'(g) For different assets, minimum correlation = {mincorr}, '
      f'maximum correlation={maxcorr:0.6f}')

# Part (h) 

nnz=count_nonzero(K)
print(f'(h) Percentage of non-zeros = {100*nnz/(n**2):0.3f}%')

# Part (i) 

Kinv = inv(K)
print('(i) Inverse of K exists; matrix is nonsingular but '
      'badly conditioned.')

# Part (j)
 
print("""(j) Since alpha = ||x||^2 where x = (R^T)^(-1) b we do not
need to invert K.
b = rand(n)
x = solve_triangular(R^T, b)
alpha = dot(x, x)""")

# Part (k)

kappa = cond(K, 2)
reK = eps;
reb = eps;
rex = kappa*(reK + reb);
nsf = floor(-log10(2*rex))

# Part (l)

print('(l) We could test if K is banded, Toeplitz or '
      'diagonally-dominant.')

# Part (m)

print('(m) Many assets have exactly zero correlation, and none '
      'have negative correlation, '
      'which seems unlikely in practice, but mathematically '
      'K is a valid correlation matrix.')