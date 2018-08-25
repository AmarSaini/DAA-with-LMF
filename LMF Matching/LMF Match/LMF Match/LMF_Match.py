import numpy as np
import nimfa
from sklearn.preprocessing import Imputer

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""

def matrix_factorization(R, P, Q, K, steps=600, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in range(steps):
        print(step)
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = np.dot(P,Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
    return P, Q.T

###############################################################################

def main():


    n = 5
    m = 4
    prefs = np.loadtxt('test5by5.csv', dtype=float, delimiter=',')

    # ATTEMPT 1
    # nmf = nimfa.Nmf(prefs, seed="nndsvd", rank=n, max_iter=12, update='euclidean', objective='fro')
    # nmf_fit = nmf()
    # R = np.dot(nmf.W, nmf.H)
    # R = np.array(R)

    # ATTEMPT 2
    #pre = Imputer(missing_values=0, strategy='mean')
    #R = pre.fit_transform(prefs)

    # ATTEMPT 3
    N = len(prefs)
    M = len(prefs[0])
    K = 4
    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)
    newP, newQ = matrix_factorization(prefs, P, Q, K)
    R = np.dot(newP, newQ.T)

    np.savetxt("R.csv", R, delimiter = ',', fmt='%f')



    # O(n^3) for scaling

    scaledR = np.zeros((n,m), int)

    for i in range(n):
        for j in range(m):
            # Some large value for initial min
            min = n*n
            index = -1
            for k in range(m):
                if(R[i][k] < min and R[i][k] != -1):
                    index = k
                    min = R[i][k]
            R[i][index] = -1
            scaledR[i][index] = j+1
                

    np.savetxt("scaledR.csv", scaledR, delimiter = ',', fmt='%f')


if  __name__ == '__main__':
    main()