import numpy as np
import sys
sys.path.append('..')  # noqa
from SMC_BASE import *
from SMC_OPT import *
from scipy.stats import multivariate_normal as Normal_PDF
from scipy import linalg

"""
Testing for SMC_OPT

P.L.Green
"""

D = 10
# Define target distribution 
p = Normal_PDF(mean=np.array([1.0 for i in range(D)]), cov=np.eye(D))

# Define initial proposal
q0 = Normal_PDF(mean=np.zeros(D), cov=np.eye(D))  

# Define proposal as being Gaussian, centered on x_cond, with identity 
# covariance matrix
q = Q_Proposal()
q.logpdf = lambda x, x_cond : -0.5 * (x - x_cond).T @ (x - x_cond)
q.rvs = lambda x_cond : x_cond + np.random.randn(D)

# Define L-kernel as being Gaussian, centered on x_cond, with identity 
# covariance matrix
L = L_Kernel()
L.logpdf = lambda x, x_cond : -0.5 * (x - x_cond).T @ (x - x_cond)
L.rvs = lambda x_cond : x_cond + np.random.randn(D)

# No. samples and iterations
N = 1000
K = 1
PCA = [True, D, False]
# SMC sampler with user-defined L-kernel
smc = SMC_BASE(N=N, D=D, p=p, q0=q0, K=K, q=q, L=L)

# SMC sampler with optimum L
smc_opt = SMC_OPT(N=N, D=D, p=p, q0=q0, K=K, q=q, PCA = PCA)


def test_sampler():
    """ For this simple example, we test that the SMC estimates of target mean
    and variance are reasonably close to the truth.

    """
    # SMC sampler with user defined L
    smc.generate_samples()

    # SMC sampler with approximately optimum L-kernel
    smc_opt.generate_samples()

    # Check estimates
    assert np.allclose(smc_opt.mean_estimate_EES[-1], p.mean, atol=0.1)
    assert np.allclose(smc_opt.var_estimate_EES[-1][0][0], p.cov[0][0],
                       atol=0.2)
    assert np.allclose(smc_opt.var_estimate[-1][1][1], p.cov[1][1],
                       atol=0.2)
    assert np.allclose(smc_opt.var_estimate[-1][0][1], p.cov[0][1],
                       atol=0.2)


def test_Neff():
    """ We'd expect that, on average, our SMC with optimum L-kernel should
    maintain a higher effective sample size that our SMC sampler with a
    'user defined' kernel.

    """

    smc.generate_samples()
    assert np.mean(smc_opt.Neff) > np.mean(smc.Neff)
smc_opt.generate_samples()
Sigma = smc_opt.sig
print(Sigma)
PCA = [False, None, False]
smc_opt = SMC_OPT(N=N, D=D, p=p, q0=q0, K=K, q=q, PCA = PCA)
smc_opt.generate_samples()
Sigma = smc_opt.sig
print(Sigma)