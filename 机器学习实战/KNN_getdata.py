#!python3
#-*-coding:utf-8-*-
import os
from numpy import *

# def img2vector(filename):
#     returnVect = zeros((1,1024))
#     fr = open(filename)
#     for i in range(32):
#         lineStr = fr.readline()
#         for j in range(32):
#             returnVect[0,32*i+j] = int(lineStr[j])
#     return returnVect
#
# hwLabels = []
# trainingFileList = os.listdir('trainingDigits')
# m = len(trainingFileList)
# trainingMat = zeros((m,1024))
# for i in range(m):
#     fileNameStr = trainingFileList[i]
#     fileStr = fileNameStr.split('.')[0]
#     classNumStr = int(fileStr.split('_')[0])
#     hwLabels.append(classNumStr)
#     trainingMat[i,:] = img2vector('trainingDigits/%s' %fileNameStr)
# print(trainingMat)

def loadFile(name):
    directory = str(os.getcwd())
    filepath = os.path.join(directory, name)
    with open(filepath,'r') as f:
        data = f.readlines()
    data = list(set(data))
    result = []
    for d in data:
        result.append(d)
    return result

a= loadFile('good.txt')
print(a)
