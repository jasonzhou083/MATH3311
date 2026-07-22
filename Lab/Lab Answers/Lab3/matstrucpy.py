from collections import namedtuple
from numpy import eye, count_nonzero, max,min
from scipy.linalg import norm, cholesky, toeplitz, tril, triu
from scipy.linalg import LinAlgError, eigvals, svdvals
from scipy.sparse import csr_matrix, issparse

s = namedtuple('s', 'dim1, dim2, square, maxval, minval, sym,'
                      'posdef, orthog, bndup, bndlo, trilo, triup, toeplitz,'
                      'evmin, evmax, svmin, svmax, cond, sparse, nnz, sparsity')
def matstruc(A, tol):
    d = dict()
    d['dim1'], d['dim2'] = A.shape
   
    if issparse(A):
        d['sparse'] = True
        A = A.todense() 
        d['nnz'] = count_nonzero(A)
    else:
        d['sparse'] = False
        d['nnz'] = count_nonzero(A)
        
    d['sparsity'] = 100 * d['nnz'] / (d['dim1']*d['dim2'])
    if d['dim1'] == d['dim2']:
        d['square'] = True
    else:
        d['square'] = False
    d['maxval'] = max(abs(A))
    d['minval'] = min(abs(A))
    if norm(A - A.T, 1) <= tol * norm(A, 1):
        d['sym'] = True
    else:
        d['sym'] = False
        
    try:
        cholesky(A)
    except LinAlgError:
        d['posdef'] = False
    else:
        d['posdef'] = True
    if norm(A.T @ A - eye(d['dim2']), 1) <= tol * norm(A, 1):
        d['orthog'] = True
    else:
        d['orthog'] = False
    # Part b) A is stored as sparse
    
    spA = csr_matrix(A)
    I, J = spA.nonzero()
    d['bndup'] = max(J-I)
    d['bndlo'] = max(I-J)
    AU = triu(A, 1)
    if norm(AU, 1) <= tol * norm(A, 1):
        d['trilo'] = True
    else:
        d['trilo'] = False
    AL = tril(A, -1)
    if norm(AL, 1) <= tol * norm(A, 1):
        d['triup'] = True
    else:
        d['triup'] = False
    T = toeplitz(A[:,0], A[0,:])
    if norm(A - T, 1) < tol * norm(A, 1):
        d['toeplitz'] = True
    else:
        d['toeplitz'] = False
    w = eigvals(A)
    d['evmin'] = min(abs(w))
    d['evmax'] = max(abs(w))
    sigma = svdvals(A)
    d['svmin'] = min(sigma)
    d['svmax'] = max(sigma)
    d['cond'] = d['svmax'] / d['svmin']

    return s(**d)