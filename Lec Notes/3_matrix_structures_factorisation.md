# Topic 3: Matrix Structures and Factorisations

This topic focuses on matrices with special structure. Recognising structure
can reduce storage, improve computational speed, and sometimes improve
numerical accuracy.

## Special Matrices

### Covariance and Correlation Matrices

Consider a vector-valued random variable

$$
X = (X_1, \ldots, X_n)^T.
$$

Each component $X_i$ is a random variable.

The **mean** of $X_i$ is

$$
\mu_i = \mathbb{E}[X_i],
\qquad
i = 1, \ldots, n.
$$

The **variance** of $X_i$ is

$$
\sigma_i^2 = \mathbb{E}[(X_i - \mu_i)^2],
\qquad
i = 1, \ldots, n.
$$

Variance measures how spread out $X_i$ is around its mean. The standard
deviation is $\sigma_i$.

The **covariance** of $X_i$ and $X_j$ is

$$
C_{ij}
=
\mathbb{E}[(X_i - \mu_i)(X_j - \mu_j)].
$$

Covariance measures whether two variables tend to increase or decrease
together.

The **covariance matrix** is

$$
C = [C_{ij}] \in \mathbb{R}^{n \times n}.
$$

Interpretation:

- $C_{ii} = \sigma_i^2$ is the variance of $X_i$.
- $C_{ij} > 0$ means $X_i$ and $X_j$ tend to vary in the same direction.
- $C_{ij} < 0$ means $X_i$ and $X_j$ tend to vary in opposite directions.

Properties:

- $C$ is symmetric.
- $C$ is positive semidefinite.

The **correlation matrix** is

$$
K = [K_{ij}] \in \mathbb{R}^{n \times n},
\qquad
K_{ij} = \frac{C_{ij}}{\sigma_i \sigma_j},
\qquad
i,j = 1, \ldots, n.
$$

Correlation normalises covariance by standard deviation, so it is unit-free.

Equivalently,

$$
K = \Sigma^{-1} C \Sigma^{-1},
\qquad
\Sigma = \operatorname{diag}(\sigma_1, \ldots, \sigma_n).
$$

Thus,

$$
\Sigma^{-1}
=
\begin{bmatrix}
1/\sigma_1 & 0 & \cdots & 0 \\
0 & 1/\sigma_2 & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & 1/\sigma_n
\end{bmatrix}.
$$

Properties:

- $K_{ii} = 1$ for $i = 1, \ldots, n$.
- $|K_{ij}| \leq 1$ for all $i,j$.
- $K$ is unit-free and easier to interpret than $C$.

Negative correlation means two variables tend to vary in opposite directions.

### Triangular Matrices

An $m \times n$ matrix $A = [a_{ij}]$ is:

- **upper triangular** if $a_{ij} = 0$ for all $i > j$.
- **lower triangular** if $a_{ij} = 0$ for all $i < j$.
- **unit lower triangular** or **unit upper triangular** if $A$ is square
  triangular and $a_{ii} = 1$ for all $i$.

Example:

$$
L =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
3 & 1 & 0 & 0 \\
-3 & 0 & 1 & 0 \\
2 & 7 & -1 & 1
\end{bmatrix},
\qquad
U =
\begin{bmatrix}
2 & 0 & -5 & 6 & 10 \\
0 & 0 & 0 & 0 & 1 \\
0 & 0 & 4 & 2 & 8 \\
0 & 0 & 0 & 7 & 3
\end{bmatrix}.
$$

- $L$ is unit lower triangular.
- $U$ is upper triangular, but not unit upper triangular.

If $A = [a_{ij}] \in \mathbb{R}^{n \times n}$ is triangular, then

$$
\det(A) = a_{11}a_{22}\cdots a_{nn}.
$$

Therefore, $A$ is invertible, or nonsingular, iff

$$
a_{ii} \neq 0
\qquad
\text{for } 1 \leq i \leq n.
$$

### Forward and Back Substitution

We solve a lower triangular system by **forward substitution** and an upper
triangular system by **back substitution**.

For a lower triangular system $Lx = b$, solve from the top row down:

$$
x_1 \rightarrow x_2 \rightarrow \cdots \rightarrow x_n.
$$

For an upper triangular system $Ux = b$, solve from the bottom row up:

$$
x_n \rightarrow x_{n-1} \rightarrow \cdots \rightarrow x_1.
$$

Example of forward substitution:

$$
\begin{aligned}
x_1 &= 3, \\
3x_1 + x_2 &= 9, \\
-3x_1 + x_3 &= -11, \\
2x_1 + 7x_2 - x_3 + x_4 &= 12.
\end{aligned}
$$

Solving from top to bottom,

$$
x_1 = 3,
\qquad
x_2 = 9 - 3x_1 = 0,
\qquad
x_3 = -11 + 3x_1 = -2,
$$

and

$$
x_4 = 12 - 2x_1 - 7x_2 + x_3 = 12 - 6 - 0 - 2 = 4.
$$

In general, for a unit lower triangular matrix
$L = [L_{ij}] \in \mathbb{R}^{n \times n}$, forward substitution to solve
$Lx = b$ takes about $n^2$ flops:

$$
x_1 = b_1,
\qquad
x_i = b_i - \sum_{j=1}^{i-1} L_{ij}x_j,
\qquad
i = 2, \ldots, n.
$$

For a general square system $Ax = b$, factorise $A$ into triangular matrices
first, for example $A = LU$, then use forward substitution followed by back
substitution.

In MATLAB:

$$
x = A \backslash b.
$$

In Python:

```python
x = numpy.linalg.solve(A, b)
```

Useful triangular matrix properties:

- $A$ is upper triangular iff $A^T$ is lower triangular.
- The product of two unit lower triangular matrices is unit lower
  triangular.
- The product of two upper triangular matrices is upper triangular.
- The inverse of a unit lower triangular matrix is unit lower triangular.
- The inverse of a nonsingular upper triangular matrix is upper triangular.

### Banded Matrices

A matrix $A = [a_{ij}]$ has:

- **lower bandwidth** $m_l$ if $a_{ij} = 0$ for all $i - j > m_l$.
- **upper bandwidth** $m_u$ if $a_{ij} = 0$ for all $j - i > m_u$.
- **total bandwidth** $m_l + m_u + 1$, the number of potentially nonzero
  diagonals.

Example:

$$
A =
\begin{bmatrix}
3 & 0 & -1 & 0 & 0 & 0 & 0 \\
-1 & -2 & 0 & 2 & 0 & 0 & 0 \\
5 & 8 & 5 & 0 & 9 & 0 & 0 \\
-2 & 0 & 2 & -7 & 0 & -1 & 0 \\
0 & 1 & 3 & 6 & -4 & 0 & -2 \\
0 & 0 & 7 & -3 & 1 & 5 & 0
\end{bmatrix}.
$$

Here $m_l = 3$, $m_u = 2$, so the total bandwidth is

$$
m_l + m_u + 1 = 3 + 2 + 1 = 6.
$$

Special cases:

- A square matrix is **diagonal** if $m_l = m_u = 0$, that is,
  $a_{ij} = 0$ for all $i \neq j$.
- A square matrix is **tridiagonal** if $m_l = m_u = 1$, that is,
  $a_{ij} = 0$ whenever $|i - j| > 1$.

For an $n \times n$ banded matrix, the number of nonzero elements is at most

$$
n
+ \sum_{i=1}^{m_l} (n - i)
+ \sum_{j=1}^{m_u} (n - j)
=
(1 + m_l + m_u)n
- \frac{m_l(m_l + 1)}{2}
- \frac{m_u(m_u + 1)}{2}.
$$

If $m_l \ll n$ and $m_u \ll n$, this is roughly

$$
(1 + m_l + m_u)n.
$$

Example: a $10000 \times 10000$ real double precision tridiagonal matrix
requires about

$$
8 \times 3 \times 10000 \text{ bytes} \approx 240 \text{ KB},
$$

compared with about

$$
8 \times 10000^2 \text{ bytes} \approx 800 \text{ MB}
$$

for a dense matrix of the same size.

### Toeplitz Matrices

A matrix $A = [a_{ij}]$ is **Toeplitz** if

$$
a_{ij} = \alpha_{j-i}
$$

for all $i$ and $j$. Equivalently, the entries are constant along each
diagonal.

Example:

```matlab
A = toeplitz([2, 1, 0, 9, 2], [2, 3, 5, 0, 1, 7])
```

In Python:

```python
A = scipy.linalg.toeplitz([2, 1, 0, 9, 2], [2, 3, 5, 0, 1, 7])
```

Both produce

$$
A =
\begin{bmatrix}
2 & 3 & 5 & 0 & 1 & 7 \\
1 & 2 & 3 & 5 & 0 & 1 \\
0 & 1 & 2 & 3 & 5 & 0 \\
9 & 0 & 1 & 2 & 3 & 5 \\
2 & 9 & 0 & 1 & 2 & 3
\end{bmatrix}.
$$

### Symmetric and Skew-Symmetric Matrices

A real matrix $A = [a_{ij}] \in \mathbb{R}^{n \times n}$ is:

- **symmetric** if $A^T = A$, equivalently $a_{ji} = a_{ij}$ for all $i,j$.
- **skew-symmetric** if $A^T = -A$, equivalently $a_{ji} = -a_{ij}$ for all
  $i,j$. In this case, $a_{ii} = 0$ for all $i$.

Every real square matrix can be decomposed as

$$
A = A_{\mathrm{sym}} + A_{\mathrm{skew}},
$$

where

$$
A_{\mathrm{sym}} = \frac{A + A^T}{2},
\qquad
A_{\mathrm{skew}} = \frac{A - A^T}{2}.
$$

If $A$ is skew-symmetric, then

$$
x^T A x = 0.
$$

For any real matrix $A$,

$$
x^T A x = x^T A_{\mathrm{sym}} x.
$$

Thus, the quadratic form only depends on the symmetric part of $A$.

### Definiteness

A matrix $A \in \mathbb{R}^{n \times n}$ is:

- **positive definite** if $x^T A x > 0$ for all nonzero $x$.
- **positive semidefinite** if $x^T A x \geq 0$ for all $x$.
- **negative definite** if $x^T A x < 0$ for all nonzero $x$.
- **negative semidefinite** if $x^T A x \leq 0$ for all $x$.
- **indefinite** if $x^T A x > 0$ for some $x$ and $y^T A y < 0$ for some
  $y$.

If $A$ is real symmetric, then all eigenvalues of $A$ are real. In this
case:

- $A$ is positive definite iff $\lambda_i > 0$ for all $i$.
- $A$ is positive semidefinite iff $\lambda_i \geq 0$ for all $i$.
- $A$ is negative definite iff $\lambda_i < 0$ for all $i$.
- $A$ is negative semidefinite iff $\lambda_i \leq 0$ for all $i$.
- $A$ is indefinite iff it has at least one positive eigenvalue and one
  negative eigenvalue.

For a non-symmetric matrix, do **not** test definiteness using the
eigenvalues of $A$ directly. Instead, test the symmetric part

$$
A_{\mathrm{sym}} = \frac{A + A^T}{2}.
$$

This works because

$$
x^T A x = x^T A_{\mathrm{sym}} x.
$$

So $A$ is positive definite, positive semidefinite, negative definite,
negative semidefinite, or indefinite according to the eigenvalues of
$A_{\mathrm{sym}}$.

Example:

$$
A =
\begin{bmatrix}
1 & 10 \\
0 & 1
\end{bmatrix}
$$

has eigenvalues $1$ and $1$, but

$$
A_{\mathrm{sym}}
=
\frac{A + A^T}{2}
=
\begin{bmatrix}
1 & 5 \\
5 & 1
\end{bmatrix}
$$

has eigenvalues $6$ and $-4$. Therefore $A$ is indefinite.

In numerical linear algebra, "positive definite" usually means symmetric
positive definite unless stated otherwise.

### Diagonal Dominance

A real matrix $A = [a_{ij}] \in \mathbb{R}^{n \times n}$ is **strictly
diagonally dominant** if

$$
a_{ii} >
\sum_{\substack{j=1 \\ j \neq i}}^n |a_{ij}|,
\qquad
i = 1, \ldots, n.
$$

If $A$ is symmetric and strictly diagonally dominant, then $A$ is positive
definite.

The converse is not true: a symmetric positive definite matrix need not be
strictly diagonally dominant.

Example:

$$
A =
\begin{bmatrix}
1 & 2 \\
2 & 5
\end{bmatrix}
$$

is positive definite because

$$
\begin{aligned}
x^T A x
&=
\begin{bmatrix}x & y\end{bmatrix}
\begin{bmatrix}
1 & 2 \\
2 & 5
\end{bmatrix}
\begin{bmatrix}x \\ y\end{bmatrix} \\
&= x^2 + 4xy + 5y^2 \\
&= (x + 2y)^2 + y^2 > 0
\end{aligned}
$$

for nonzero $(x,y)$. However, $A$ is not strictly diagonally dominant.

### Orthogonal Matrices

A matrix $A \in \mathbb{R}^{n \times n}$ is **orthogonal** if

$$
A^T A = I_n.
$$

Writing

$$
A = [a_1 \ a_2 \ \cdots \ a_n],
$$

where $a_j$ is the $j$th column of $A$, $A$ is orthogonal iff the columns
are orthonormal:

$$
a_j^T a_k = a_j \cdot a_k = \delta_{jk}
=
\begin{cases}
1, & j = k, \\
0, & j \neq k.
\end{cases}
$$

If $A$ is orthogonal, then:

- its columns are linearly independent, so $\operatorname{rank}(A) = n$.
- $A$ is nonsingular.
- $A^{-1} = A^T$.
- $\kappa_2(A) = 1$, which is ideal conditioning.

Orthogonal matrices preserve inner products and Euclidean norms:

$$
A \text{ is orthogonal}
\Longleftrightarrow
(Ax) \cdot (Ay) = x \cdot y
\Longleftrightarrow
\|Ax\|_2 = \|x\|_2.
$$

### Permutation Matrices

A **permutation matrix** $P \in \mathbb{R}^{n \times n}$ is obtained by
permuting the rows of $I_n$.

Permutation matrices are orthogonal:

$$
P^T P = I_n = PP^T.
$$

Applying $P$ to a matrix $A$ permutes the rows of $A$:

$$
PA.
$$

In MATLAB, if `p` is a permutation of `1:n`, then `A(p,:)` gives the same
result as $PA$.

In Python, using zero-based indexing, `A[p, :]` gives the same result as
$PA$.

Example: swapping rows $2$ and $4$ of a $4 \times 4$ matrix uses

$$
P =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0
\end{bmatrix}.
$$

Then

$$
PA =
\begin{bmatrix}
a_{11} & a_{12} & a_{13} & a_{14} \\
a_{41} & a_{42} & a_{43} & a_{44} \\
a_{31} & a_{32} & a_{33} & a_{34} \\
a_{21} & a_{22} & a_{23} & a_{24}
\end{bmatrix}.
$$

## Matrix Factorisations

### LU Factorisation

An **LU factorisation** of $A \in \mathbb{R}^{n \times n}$ is

$$
A = LU,
$$

where $L$ is unit lower triangular and $U$ is upper triangular.

If $A = LU$, then

$$
Ax = LUx = b.
$$

Let

$$
y = Ux.
$$

Then solve the system in two triangular steps:

1. Solve $Ly = b$ by forward substitution.
2. Solve $Ux = y$ by back substitution.

This is equivalent to Gaussian elimination.

When it exists, the LU factorisation of a nonsingular matrix is unique.

LU factorisation does not always exist without row swaps. For example,

$$
\begin{bmatrix}
0 & 1 \\
1 & 3
\end{bmatrix}
$$

cannot be written as $LU$ with $L$ unit lower triangular, because the first
pivot would be zero. Swapping rows gives

$$
\begin{bmatrix}
1 & 3 \\
0 & 1
\end{bmatrix},
$$

which is already upper triangular.

In general, **partial pivoting** may produce a permutation matrix $P$, a unit
lower triangular matrix $L$, and an upper triangular matrix $U$ such that

$$
PA = LU.
$$

For a nonsingular $A$, solve $Ax = b$ using

$$
PAx = Pb
\quad \Longrightarrow \quad
LUx = Pb.
$$

Then:

1. Solve $Ly = Pb$ by forward substitution.
2. Solve $Ux = y$ by back substitution.

Partial pivoting ensures

$$
|\ell_{ij}| \leq 1
\qquad
\text{for } i > j,
$$

which helps control round-off errors.

Costs:

- Computing $PA = LU$ costs about $\frac{2}{3}n^3$ flops.
- Solving the two triangular systems costs about $2n^2$ flops.
- For double precision real arithmetic, memory is about $8(n^2+n)$ bytes.

Using LU factorisation to solve $Ax=b$ is faster than computing $A^{-1}$ and
forming $x = A^{-1}b$.

### Cholesky Factorisation

If $A \in \mathbb{R}^{n \times n}$ is symmetric positive definite, then

$$
A = R^T R,
$$

where $R$ is upper triangular. This is the **Cholesky factorisation**.

To solve $Ax = b$:

$$
Ax = R^T R x = b.
$$

Let

$$
y = Rx.
$$

Then:

1. Solve $R^T y = b$ by forward substitution.
2. Solve $Rx = y$ by back substitution.

Costs:

- Computing $R$ costs about $\frac{1}{3}n^3$ flops, about half the cost of
  LU factorisation.
- The triangular solves cost about $n^2$ flops each.
- Cholesky does not require row reordering.

Cholesky factorisation is also an efficient way to check whether $A$ is
positive definite.

MATLAB:

```matlab
[R, p] = chol(A)  % p = 0 means A is positive definite
```

Python:

```python
R = scipy.linalg.cholesky(A)
```

### QR Factorisation

Let $A \in \mathbb{R}^{m \times n}$ with $m \geq n$.

If $\operatorname{rank}(A) = n$, then $A$ has a QR factorisation

$$
A =
Q
\begin{bmatrix}
R \\
0
\end{bmatrix},
$$

where:

- $Q \in \mathbb{R}^{m \times m}$ is orthogonal.
- $R \in \mathbb{R}^{n \times n}$ is nonsingular upper triangular.
- $0 \in \mathbb{R}^{(m-n) \times n}$.

Writing

$$
Q = [Y \ Z],
$$

where $Y \in \mathbb{R}^{m \times n}$ and
$Z \in \mathbb{R}^{m \times (m-n)}$, we get

$$
A = YR.
$$

This is the **economy-size QR factorisation**.

If $A$ is rank deficient, column pivoting is required:

$$
AP =
Q
\begin{bmatrix}
R \\
0
\end{bmatrix}
= YR,
$$

where $P$ is a column permutation matrix.

The pivoting is chosen so that

$$
|r_{11}| \geq |r_{22}| \geq \cdots \geq |r_{nn}|.
$$

In exact arithmetic, the rank of $A$ is the number of nonzero diagonal
entries of $R$. In numerical computation, very small diagonal entries
indicate numerical rank deficiency.

The economy-size QR factorisation costs about

$$
2mn^2 - \frac{2}{3}n^3
$$

flops.

### Singular Value Decomposition

Let $A \in \mathbb{R}^{m \times n}$ with $m \geq n$.

An **SVD** of $A$ is

$$
A =
U
\begin{bmatrix}
\Sigma \\
0
\end{bmatrix}
V^T,
$$

where:

- $U \in \mathbb{R}^{m \times m}$ is orthogonal.
- $V \in \mathbb{R}^{n \times n}$ is orthogonal.
- $\Sigma = \operatorname{diag}(\sigma_1,\ldots,\sigma_n)$.
- The singular values satisfy
  $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_n \geq 0$.

The rank of $A$ is the number of positive singular values:

$$
\operatorname{rank}(A) = r.
$$

If $r = \operatorname{rank}(A)$, then

$$
\Sigma_r = \operatorname{diag}(\sigma_1,\ldots,\sigma_r)
$$

is invertible, and

$$
A = \sum_{j=1}^r \sigma_j u_j v_j^T.
$$

Terminology:

- $\sigma_1,\ldots,\sigma_n$ are the **singular values**.
- $u_1,\ldots,u_m$ are the **left singular vectors**.
- $v_1,\ldots,v_n$ are the **right singular vectors**.

They satisfy

$$
Av_i = \sigma_i u_i,
\qquad
u_i^T A = \sigma_i v_i^T.
$$

For numerical rank, MATLAB `rank(A)` uses a tolerance based on

$$
\max(m,n)\epsilon\sigma_1,
$$

where $\epsilon$ is machine precision. Python `numpy.linalg.matrix_rank(A)`
uses the same idea.

### Condition Number from Singular Values

Let $A \in \mathbb{R}^{n \times n}$ have full rank, and let

$$
A = U\Sigma V^T
$$

be its SVD. Then

$$
A^T A = V\Sigma^2 V^T,
\qquad
\Sigma^2 = \operatorname{diag}(\sigma_1^2,\ldots,\sigma_n^2).
$$

Thus, the eigenvalues of $A^T A$ are

$$
\sigma_1^2,\ldots,\sigma_n^2.
$$

Therefore,

$$
\|A\|_2 = \sigma_1.
$$

Since

$$
A^{-1} = V\Sigma^{-1}U^T,
\qquad
\Sigma^{-1} = \operatorname{diag}(1/\sigma_1,\ldots,1/\sigma_n),
$$

we have

$$
\|A^{-1}\|_2 = \frac{1}{\sigma_n}.
$$

Hence,

$$
\kappa_2(A) = \frac{\sigma_1}{\sigma_n}.
$$

If $A \in \mathbb{R}^{m \times n}$ with $m > n$ and full column rank, the
same formula is used:

$$
\kappa_2(A) = \frac{\sigma_1}{\sigma_n}.
$$

For symmetric positive definite $A$ with eigenvalues

$$
0 < \lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_n,
$$

the $2$-norm condition number is

$$
\kappa_2(A) = \frac{\lambda_n}{\lambda_1}.
$$
