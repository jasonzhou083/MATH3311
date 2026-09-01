from matstrucpy import matstruc
from numpy import array
from laplace0 import laplace0

tol = 1e-13

A1 = array([[ 2, -1,  0,  0],
            [-1,  2, -1,  0],
            [ 0, -1,  2, -1],
            [ 0,  0, -1,  2]])
s1 = matstruc(A1, tol)
d1 = s1._asdict()
print('First matrix:\n')
for key, val in d1.items():
    print(f'\t{key:8s}: {val}')

print('\nSecond matrix:\n')
### BEGIN SOLUTION
A2 = laplace0()
s2 = matstruc(A2, tol)
d2 = s2._asdict()
for key, val in d2.items():
    print(f'\t{key:8s}: {val}')
### END SOLUTION