# Linear Algebra Notes

> **About this file**
>
> This file is a compact reference for useful linear algebra identities, dimension rules, and common matrix/vector properties.
>
> When adding new notes:
>
> - State the rule clearly in mathematical notation.
> - Include the conditions under which it is valid.
> - Show the relevant matrix or vector dimensions when helpful.
> - Keep explanations short and focused.
> - Add a small example only when the rule may be easy to misuse.
> - Group related rules under a suitable heading.

## Transpose Rules

The transpose of a matrix product reverses the order:

$$
(AB)^T = B^T A^T.
$$

This rule applies when the product $AB$ is defined. I f
$A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{n \times p}$, then
$AB \in \mathbb{R}^{m \times p}$ and

$$
(AB)^T \in \mathbb{R}^{p \times m},
\qquad
B^T A^T \in \mathbb{R}^{p \times m}.
$$

Therefore, for a matrix $A$ and column vector $v$,

$$
(Av)^T = v^T A^T.
$$

This special case applies when $A \in \mathbb{R}^{m \times n}$ and
$v \in \mathbb{R}^{n}$ is a column vector, so $Av \in \mathbb{R}^{m}$.

## Singular Matrices

A square matrix $A \in \mathbb{R}^{n \times n}$ is **singular** if it does not have an inverse.

Equivalent conditions:
- $A^{-1}$ does not exist.
- $\det(A) = 0$.
- $Ax = 0$ has a nonzero solution $x \neq 0$.
- The columns of $A$ are linearly dependent.

## Determinant Rules

For square matrices $A,B \in \mathbb{R}^{n \times n}$,

$$
\det(AB) = \det(A)\det(B).
$$

Useful consequences:

- $\det(A^T) = \det(A)$.
- If $\lambda_1, \ldots, \lambda_n$ are the eigenvalues of $A$, counted
  with algebraic multiplicity, then
  $$
  \det(A) = \lambda_1\lambda_2\cdots\lambda_n.
  $$
- If $A$ is nonsingular, then
  $$
  \det(A^{-1}) = \frac{1}{\det(A)}.
  $$
- $\det(A^k) = \det(A)^k$.
- $AB$ is nonsingular iff both $A$ and $B$ are nonsingular.

For a Cholesky factorisation

$$
K = R^T R,
$$

we get

$$
\det(K)
= \det(R^T)\det(R)
= \det(R)^2.
$$

Since $R$ is triangular,

$$
\det(R) = \prod_i r_{ii},
$$

so

$$
\det(K) = \left(\prod_i r_{ii}\right)^2.
$$

## Positive Semidefinite Matrices

A real symmetric matrix $A$ is **positive semidefinite** if

$$
x^T A x \geq 0
$$

for every vector $x$.

For a real symmetric matrix, this is equivalent to all eigenvalues of $A$
being non-negative.

If $x^T A x > 0$ for every nonzero $x$, then $A$ is **positive definite**.

For any real matrix $A \in \mathbb{R}^{m \times n}$,

$$
A^T A
$$

is always symmetric positive semidefinite, since

$$
x^T A^T A x = (Ax)^T(Ax) = \|Ax\|_2^2 \geq 0.
$$
