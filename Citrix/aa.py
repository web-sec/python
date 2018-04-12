#*-*coding:utf-8*-*
import pandas as pd
import re
df = pd.read_csv("../info/printing.csv",sep='\t')
print(df['CaseNumber'])
