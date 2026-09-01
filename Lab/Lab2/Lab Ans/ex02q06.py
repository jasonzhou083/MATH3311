
from symchkSol import  symchk
from numpy import finfo, inf
from numpy.random import rand, randn
from scipy.linalg import norm

# Test 1:  Non-square matrix

A1 = rand(4, 3)
chk1 = symchk(A1)

# Test 2: Matrix square, but not symmetric

A = randn(5,5)

# Test 3: Symmetric matrix, default tolerance

B = A.T@A # A matrix of the form A^T A is always symmetric 

chk3 = symchk(B)

# Test 4: Symmetric part, default tolerance

# A square matrix  has symmetric part S = (A + A^T)/2 and
# skew-symmetric part K = (A - A^T)/2  with A = S + K

S = (A + A.T)/2
chk4 = symchk(S)
K = (A - A.T)/2
chk4a = symchk(K)
chkSK = norm(A-(S+K), inf)

# Test 5: Same matrix, larger tolerance

tol = 1e-14
chk5 = symchk(A, tol)
# Check actual norm
chk_nrm = norm(A-A.T, inf)

# Test 6: Illegal tolerance

tol1 = finfo(float).eps
chk6 = symchk(A, tol1)