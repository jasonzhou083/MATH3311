from scipy.io import loadmat
from numpy import save

d = loadmat('corr.mat')
K = d['K']
save('corr.npy', K, allow_pickle=False)
