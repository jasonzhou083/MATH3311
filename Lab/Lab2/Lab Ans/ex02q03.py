from numpy import array, inf
from scipy.linalg import norm, eigvals

A = array([[  3, -2,  0,  5],
           [  1,  8,  7,  0],
           [ -9,  5,  1,  2],
           [  3, -2,  0,  5],
           [  3, -4,  0,  5]])


print('(a) The matrix A:')
print(A)

# Part a)
print(f'\n||A||_1 = {norm(A,1)}, ||A||_infty = {norm(A,inf)}, ||A||_2 = {norm(A,2)}')

# Part b) i-
B = A[0:4,0:4]
print('\n(b)The (sub)matrix B:')
print(B)

# ii- 

print(f'\n||B||_1 = {norm(B,1)}, ||B||_infty = {norm(B,inf)}, ||B||_2 = {norm(B,2)}')


# iii-

eigenvalues = eigvals(B)
print('\nEigenvalues of B are')
print(eigenvalues)
k = max(abs(eigenvalues))

print(f'|lambda_max|={k}')

# print(f'|lambda_max|  and ||B||_2  are not equal.')
