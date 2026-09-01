from scipy.linalg import norm
from numpy import inf, array

x = array([-9, 5, 1, -4, 12, -7])

# Part (a) 
print(f'(a) ||x||_1 = {norm(x, 1):}')

# Part (b) 
print(f'(b) ||x||_2 = {norm(x, 2):0.10f}')

# Part (c) 
print(f'(c) ||x||_infty = {norm(x, inf):}')
