import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import os


def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding,) as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    print('has read {length} data.'.format(length=len(data)))
    return data

#获取指定列名的全部信息；
#所有的列名'Id', 'CaseNumber', 'Service Product Consolidated', 'ProblemType', 'Date Created', 'Age/TTC', 'Severity', 'Product Component', 'Status', 'Product Version', 'Subject', 'Description', 'Resolution', 'Cause'
def GetOneColumnData(source,column_name):
    column_list = source[0]
    column_data = []
    if column_name not in column_list:
        print('{column_name} not exists!'.format(column_name=column_name))
    else:
        column_index = source[0].index(column_name)
        for i in source[1:]:
            column_data.append(i[column_index])
    print('get {column_length} {column_name} data!'.format(column_length=len(column_data),column_name=column_name))
    return column_data

def WriteTrainDataToCsv(csv_path,algorithm,data_quantity, component_type, accuracy, precision, recall, f1, auc):
    #如果没这个文件，第一行先生成列名
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            first_column = ['algorithm','data_quantity', 'component_type', 'accuracy', 'precision', 'recall', 'f1', 'auc']
            writer = csv.writer(f)
            writer.writerow(first_column)
    #写入训练后的测试数据
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([algorithm,data_quantity,component_type, accuracy, precision, recall, f1, auc])
        print('successfully writing!')
    return

#获取所有component的类别
def GetALLDiffKindOfComponents(component_list):
    kinds = []
    for i in component_list:
        if i not in kinds:
            kinds.append(i)
    return kinds

#计算这个种类的component的数量
def CalThisKindComponentAccount(component_list,component_name):
    quantity = 0
    for i in component_list:
        if i == component_name:
            quantity += 1
    return quantity

#获取列表中数值最大的前n个数的下标，返回的是下标的数组
def GetTopNProba(l,n):
    top = []
    for i in range(n):
        top.append(l.index(max(l)))
        l[top[-1]] = 0
    return top
#读取文件
csv_data = ReadCSVFile('../../info/rawdata.csv')
for i in csv_data[-1::-1]:
    if i == []:
        csv_data.remove(i)

kind = []
data = []
kindname=''
for i in csv_data:
    if i[0] != '':
        kindname=i[0]
    kind.append(kindname)
    data.append(i[1])



#计算文本TF-IDF
vectorizer = TfidfVectorizer(stop_words='english',sublinear_tf=True)
X = vectorizer.fit_transform(data)  # 计算每个词语的tf-idf权值
y = kind

# 切割训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# 使用LR模型训练
lgs = LogisticRegression()
lgs.fit(X_train, y_train)


p = lgs.predict(X_test)
accuracy = metrics.accuracy_score(y_test, p)
print(X_test)
