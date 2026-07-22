from numpy import log, pi, exp, finfo, float32, float64

print('(a) x = 7 log(pi)')

### BEGIN SOLUTION
x = 7 * log(pi)
print(f'(b) x = {x:0.14f}')

chk_equal = ( pi**7 == exp(x) )
print('(c) chk_equal =', chk_equal)
      
abs_error = abs(pi**7 - exp(x))
print(f'(d) absolute error = {abs_error:.3e}')
      
eps_sgl = finfo(float32).eps
eps_dbl = finfo(float64).eps
print(f'(e) Estimated rounding errors')
print(f'\tSingle precision: {pi**7 * eps_sgl:0.4e}')
print(f'\tDouble precision: {pi**7 * eps_dbl:0.4e}')
### END SOLUTION