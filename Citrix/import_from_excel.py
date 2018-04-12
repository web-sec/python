#*-*coding:utf-8*-*
import pandas as pd
import re
df = pd.read_csv("../info/all.csv")
#df = pd.read_csv("info/printing.csv")

# problem_type = df['ProblemType']
# description = df['Description']
# nan = float('nan')
# print(len(problem_type))
# for i in range(len(problem_type)-1,-1,-1):
#     if type(description[i]) == type(nan):
#         print(i)
#         del (description[i])
#         del (problem_type[i])
#     # else:
#     #     description[i] = re.sub('[^a-zA-Z]','',description[i])
#     #     if description[i] == '':
#     #         del(description[i])
#     #         del(problem_type[i])
# print(len(description))
# print(len(problem_type))
problem_type = df['ProblemType']
