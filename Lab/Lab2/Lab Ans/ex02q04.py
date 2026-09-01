from numpy import inf, identity
from scipy.linalg import hilbert
from numpy.linalg import cond 

alpha=4
n=5

# Part a)
A = alpha*identity(n, dtype="int")
CondA1=cond(A,1)
CondA2=cond(A,2)
CondAinf=cond(A,inf)

print('(a) Cond_1(A) =' f'{CondA1:12.1e}'   '\nCond_2(A) =' f'{CondA2:12.1e}' 
      '\nCond_inf(A) =' f'{CondAinf:12.1e}')

# Part b)
print('(b)' f"{'n':>3} {'Cond_1(H)':>12} {'Cond_2(H)':>12} {'Cond_inf(H)':>12}\n")
for n in [5, 10, 15]:
    H = hilbert(n)
    print(f'{n:4}', end=' ')
    for p in [1, 2, inf]:
        condH = cond(H,p)  
        print(f'{condH:>12.3e}', end=' ')
    print()



