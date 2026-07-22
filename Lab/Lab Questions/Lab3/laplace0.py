
from numpy import zeros
from scipy.sparse import spdiags, eye, kron

def laplace0(n=5, m=8):
    """
    Sparse matrix from the 5 point discretization of the 2D Laplacian.   

    Parameters
    ----------
    n : integer, optional
        Number of intervals along the x-axis is n+1. The default is 5.
    m : integer, optional
        Number of intervals along the y-axis is m+1. The default is 8.

    Returns
    -------
    A : csc_matrix
        A is (nm) x (nm).
    """
    
    datax = zeros((3, n))
    datax[0,:] = -1
    datax[1,:] = 2
    datax[2,:] = -1
    Ax = spdiags(datax, [-1, 0, 1], n, n)
    datay = zeros((3, m))
    datay[0,:] = -1
    datay[1,:] = 2
    datay[2,:] = -1  
    Ay = spdiags(datay, [-1, 0, 1], m, m)
    Ix = eye(n)
    Iy = eye(m)
    A = kron(Ax, Iy) + kron(Ix, Ay)
    A=A.todense()
    return A
   # return A.tocsc()


