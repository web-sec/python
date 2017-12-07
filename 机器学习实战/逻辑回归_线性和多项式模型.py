#import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import minimize,fmin_bfgs
def loaddata(file, delimeter):
    data = np.loadtxt(file, delimiter=delimeter)
    return(data)

def sigmoid(z):
    return(1 / (1 + np.exp(-z)))

def costFunction(theta, X, y):
    m = y.size
    h = sigmoid(X.dot(theta))
    J = -1.0*(1.0/m)*(np.log(h).T.dot(y)+np.log(1-h).T.dot(1-y))
    if np.isnan(J[0]):
        return(np.inf)
    return J[0]

def gradient(theta, X, y):
    m = y.size
    h = sigmoid(X.dot(theta.reshape(-1,1)))
    grad =(1.0/m)*X.T.dot(h-y)
    return(grad.flatten())
#----------------------data1.txt-------------------
# data = loaddata('data1.txt', ',')
# X = np.c_[np.ones((data.shape[0],1)), data[:,0:2]]
# y = np.c_[data[:,2]]
# initial_theta = np.zeros(X.shape[1])

# cost = costFunction(initial_theta, X, y) #ones cost
# grad = gradient(initial_theta, X, y) #ones grad

# result = fmin_bfgs(costFunction, initial_theta, fprime=gradient, args=(X,y)) # use Quasi-Newton Methods
# res = minimize(costFunction, initial_theta, args=(X,y), jac=gradient, options={'maxiter':400})
# print(res)
#----------------------data1.txt-------------------

#----------------------data2.txt-------------------
def map_feature(x1, x2):
    '''''
    Maps the two input features to polonomial features.
    Returns a new feature array with more features of
    X1, X2, X1 ** 2, X2 ** 2, X1*X2, X1*X2 ** 2, etc...
    '''
    x1.shape =(x1.size,1)
    x2.shape =(x2.size,1)
    degree =6
    mapped_fea = np.ones(shape=(x1[:,0].size,1))
    m, n = mapped_fea.shape
    for i in range(1, degree +1):
        for j in range(i +1):
            r =(x1 **(i - j))*(x2 ** j)
            mapped_fea = np.append(mapped_fea,r, axis=1)
    return mapped_fea

def costFunctionReg(theta, reg, *args):
    m = y.size
    h = sigmoid(XX.dot(theta))
    J = -1.0*(1.0/m)*(np.log(h).T.dot(y)+np.log(1-h).T.dot(1-y)) + (reg/(2.0*m))*np.sum(np.square(theta[1:]))
    if np.isnan(J[0]):
        return(np.inf)
    return(J[0])

def gradientReg(theta, reg, *args):
    m = y.size
    h = sigmoid(XX.dot(theta.reshape(-1,1)))
    grad = (1.0/m)*XX.T.dot(h-y) + (reg/m)*np.r_[[[0]],theta[1:].reshape(-1,1)]
    return(grad.flatten())

data = loaddata('data2.txt', ',')
X = np.c_[np.ones((data.shape[0],1)), data[:,0:2]]
y = np.c_[data[:,2]]

XX = map_feature(X[:,0], X[:,1])
initial_theta = np.zeros(XX.shape[1])
# initial_theta = np.zeros(XX.shape[1])
# costFunctionReg(initial_theta, 1, XX, y)

#res = fmin_bfgs(costFunction, initial_theta, fprime=gradient, args=(XX,y))
res = minimize(costFunction, initial_theta, args=(XX,y), jac=gradient, options={'maxiter':400})
print(res.x)
#----------------------data2.txt-------------------
