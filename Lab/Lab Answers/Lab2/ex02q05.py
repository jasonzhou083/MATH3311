from numpy import finfo, log10, floor


# A known "exactly" means relative error in A is equal to
# relative machine precision eps
# Relative error is zero only when all elements are integers or 
# combinations of powers of 2

reA = finfo(float).eps

# RHS is know to 8 significant figures
reb = 0.5e-08

# Part a) i
Anrm = 1.2e01 #norms of A
AInrm = 3.9e03 #norms of invA
Acond1 = Anrm*AInrm

# Estimate of relative error in computed solution x
rex1 = Acond1 * (reA + reb)

# Number of significant figures: rex < 0.5*10^(-k)
nsf1 = floor(-log10(2*rex1))

# ii  Given A is symmetric and ordered eigenvalues

evmin = 0.00031 #smallest magnitude eigenvalue
evmax = 198.2 #largest magnitude eigenvalue
Acond2 = evmax/evmin # || A ||_2 = evmax,  || inv(A) ||_2 = 1 /evmin 
# Estimate of relative error in computed solution x
rex2 = Acond2 * (reA + reb)
# Number of significant figures: rex < 0.5*10^(-k)
nsf2 = floor(-log10(2*rex2))

# iii   Given rcond
rc = 9.9010e-12 #Reciprocal condition number
Acond3 = 1 / rc
rex3 = Acond3 * (reA + reb)

# Number of significant figures: rex < 0.5*10^(-k)
# Any value of rex > 0.5e-01 will give 0 significant figures
nsf = floor(-log10(2*rex3))

print('(a) Number of significant figures in x' '\n i    ' f'{nsf1:}'   '\n ii   ' f'{nsf2:}' 
      '\n iii ' f'{nsf:}')

# Part b) Required accuracy in RHS

# Find relative error in b to get computed solution to Ax = b with 6 significant figures
# re(x) = cond(A) * (re(A) + re(b)) <=> re(b) = re(x)/cond(A) - re(A) 
rex = 0.5e-6
# Part i)
reb1 = rex/Acond1 - reA
# Part ii)
reb2 = rex/Acond2 - reA
# Part iii) 
# Negative value for reb3 => impossible to achieve requested accuracy in x
# for this large a condition number for A
reb3 = rex/Acond3 - reA

print('(b) i- Relative error in b =' f'{reb1:12.4e}'   '\n ii- Relative error in b=' f'{reb2:12.4e}' 
      '\n iii- Relative error in b =' f'{reb3:12.4e}')