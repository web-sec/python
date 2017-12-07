#!python3
#-*-coding:utf-8-*-
import numpy
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

def sigmoid(inX):
    return 1.0 / (1 + numpy.exp(-inX))

data = numpy.loadtxt('data1.txt',delimiter=',')
X = data[:,0:2]
Y = data[:,2]
x = X[:,0]
y = X[:,1]
for i in range(len(Y)):
    if Y[i] == 0.0:
        plt.scatter(x[i],y[i],c='r',marker='x')
    else:
        plt.scatter(x[i],y[i],c='blue',marker='.')



X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3,random_state=42)
lgs = LogisticRegression()
lgs.fit(X_train,Y_train)
a = lgs.coef_[0]
b = lgs.intercept_[0]
predicted = lgs.predict(X_test)
print(metrics.f1_score(Y_test,predicted))
print(a,b)

# a=[0.20623172,0.2014716]
# b=-25.16133401
x = numpy.arange(20, 100, 1)
y = (-b - a[0] * x) / a[1]
plt.plot(x,y)
plt.show()
