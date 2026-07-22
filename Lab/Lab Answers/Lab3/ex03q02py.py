from laplace0 import laplace0
from scipy.linalg import cholesky, norm, qr, eigvalsh, LinAlgError, svd, inv, lu,  toeplitz
from scipy.sparse import eye, issparse
from numpy import  prod, finfo
from matplotlib.pyplot import subplot, spy, figure, title, semilogy, grid



# Part (b) 

A = laplace0()

# Part (c) 
nrows, ncols = A.shape
print(f'(c) Matrix A is {nrows} x {ncols}.')

Asparse=issparse(A)

if Asparse:
    print('A is stored as a sparse matrix')
else:
    print('A is not stored as a sparse matrix')

figure(1)
spy(A, markersize=1)
title('Spy plot of A')

delta = abs(A - A.T).max()
print(f'\tmax|a_ij - a_ji| = {delta} so A is symmetric.')
try:
    R = cholesky(A)
except LinAlgError:
    print('\tA is not positive-definite')
else:
    print('\tA is positive-definite')
    
delta = A * A.T - eye(nrows)
print(f'\t||A A^T - I||_1 = {norm(delta,1)} so '
      ' A is not orthogonal')

I, J = A.nonzero()
upper_bw = (J-I).max()
lower_bw = (I-J).max()
print(f'\tA has upper bandwidth = {upper_bw}, '
      f'lower bandwidth = {lower_bw}, '
      f'total bandwidth = {upper_bw+1+lower_bw}.')

# Part c) v. Toeplitz
T = toeplitz(A[:,0], A[0,:])

eps = finfo(float).eps
if norm(A-T) < eps * nrows:
    print('A is toeplitz')
else:
    print('A is not toeplitz')
        
# Part c) vi. Eigenvalues and singular values
    
w = eigvalsh(A)
figure(2) 
subplot(2, 1, 1)
semilogy(w, '.')
grid(True)
title('Eigenvalues of A')


U, s, VT = svd(A)
subplot(2, 1, 2)
semilogy(s, '.')
grid(True)
title('Singular values of A')


# Part c) vii. Determinant

print(f'\tdet(A) = {prod(w):0.4e}')

# Part c) viii. Inverse

Ainv = inv(A);
figure(3)
spy(Ainv, markersize=1)
title('Spy plot of A^{-1}')

# Part c) ix. Factorizations

# LU factorization
Pt, L, U = lu(A)
P = Pt.T
LUchk = norm(P*A-L@U, 1)
Pchk = norm(P-eye(nrows), 1)
print('Part c) ix. Factorizations')
print(f'LU: || PA - LU ||_1 = {LUchk}')

if Pchk == 0:
    print('P=I, no reordering is used')
else:
    print(f'The permutation matrix P={P}')

# Cholesky factorization
Cholchk = norm(A-R.T@R, 1)
print(f'Cholesky: ||A - R^T R||_1 = {Cholchk}')


# QR factorization
Q, R1 = qr(A)
QRchk = norm(A-Q@R1, 1)
print(f'QR: ||A - QR ||_1 = {QRchk}')

# SVD factorization
U, S, VT = svd(A)
SVDchk = norm(A-U*S@VT, 1)
print(f'SVD: ||A - USV^T ||_1 = {SVDchk}')



figure(4) 
subplot(2, 1, 1)
spy(Q, markersize=1)
title('The orthogonal factor Q')

subplot(2, 1, 2)
spy(R1, markersize=1)
title('The upper triangular factor R')
