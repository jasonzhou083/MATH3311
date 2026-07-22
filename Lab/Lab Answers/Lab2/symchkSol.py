from numpy import maximum, any, finfo, float32, float64, ndarray


def symchk(A, tol=None):
    """
    Test if a matrix is symmetric.

    Parameters
    ----------
    A : NumPy matrix of type float32 or float64. 

    tol : float, optional
        The relative tolerance for violation of symmetry. The default is None,
        which case the function sets tol to 10 n^2 eps.

    Raises
    ------
    ValueError
        If A is not a floating-point matrix or if tol is negative

    Returns
    -------
    bool
        True if and only if |A[i,j] - A[j,i]| <= tol max(|A[i,j]|,|A[j,i]|)
        for all i and j.
    """
    if (not isinstance(A, ndarray)) or (len(A.shape) != 2):
        raise ValueError('A must be a NumPy Matrix')
    m, n = A.shape
    if m != n:
        return False
    if A.dtype == float32:
        eps = finfo(float32).eps
    elif A.dtype == float64:
        eps = finfo(float64).eps
    else:
        raise ValueError('Matrix must be float32 or float64')
    if tol is None:
        tol = 10 * eps * n**2
    if (not isinstance(tol, float)) or (tol < 0):
        raise ValueError('tol must be a positive float')
    delta = abs(A - A.T)
    M = maximum(abs(A), abs(A.T))
    if any(delta > tol * M):
        return False
    else:
        return True
