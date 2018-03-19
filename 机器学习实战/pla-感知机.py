#*-coding:utf-8-*
import numpy as np
def MakeData(w,n):
    weight = np.array(w)
    numFeatures = len(w)
    data = np.zeros((n,(numFeatures+1)))
    for i in range(n):
        x = np.random.rand(1,numFeatures)*20-10
        #print(x)
        sumx = np.sum(w*x)
        #print(sumx)
        if sumx>0:#|X点向量|*|法向量|*cos0：点乘大于0，说明改点与直线的法向量夹角小于90度，在一边，小于零则在另一边
            data[i] = np.append(x,1)
        else:
            data[i] = np.append(x,-1)
    return data


def plotData(dataSet,weights):
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    w = weights
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Linear separable data set')
    plt.xlabel('X')
    plt.ylabel('Y')
    labels = np.array(dataSet[:,2])
    idx_1 = np.where(dataSet[:,2]==1)
    p1 = ax.scatter(dataSet[idx_1,0], dataSet[idx_1,1],
        marker='o', color='g', label=1, s=20)
    idx_2 = np.where(dataSet[:,2]==-1)
    p2 = ax.scatter(dataSet[idx_2,0], dataSet[idx_2,1],
        marker='x', color='r', label=2, s=20)
    x = w[0][0] / abs(w[0][0]) * 10
    y = w[0][1] / abs(w[0][0]) * 10
    ann = ax.annotate(u"",xy=(x,y),
        xytext=(0,0),size=20, arrowprops=dict(arrowstyle="-|>"))
    ys = (-12 * (-w[0][0]) / w[0][1], 12 * (-w[0][0]) / w[0][1])
    ax.add_line(Line2D((-12, 12), ys, linewidth=1, color='blue'))
    plt.legend(loc = 'upper right')
    plt.show()

def train(dataSet):
    ''' (array, boolean) -> list

    Use dataSet to train a perceptron
    dataSet has at least 2 lines.

    '''
    numLines = dataSet.shape[0]
    numFeatures = dataSet.shape[1]
    w = np.zeros((1, numFeatures - 1))         # initialize weights
    separated = False

    i = 0;
    while not separated and i < numLines:
        if dataSet[i][-1] * np.sum(w * dataSet[i,0:-1]) <= 0:
            w = w + dataSet[i][-1] * dataSet[i,0:-1]
            separated = False
            i = 0;
        else:
            i += 1
    return w

dataSet = MakeData([4,3],100)
w = train(dataSet)
print(w)
plotData(dataSet,w)
