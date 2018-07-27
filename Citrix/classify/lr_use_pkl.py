# coding:utf-8
# !python3
import pickle
from sklearn.externals import joblib

# 读取训练好的TF-IDF词袋模型
with open('tfidf_DR.pkl', 'rb') as f:
    vectorizer_tfidf_DR = pickle.load(f)
with open('tfidf_VDA_DRC.pkl', 'rb') as f:
    vectorizer_tfidf_VDA_DRC = pickle.load(f)

# 读取训练好的lr模型
lr = joblib.load('lr_DR.pkl')
lr_vda = joblib.load('lr_VDA_DRC.pkl')
# rf = joblib.load('.pkl')

# 将多个模型放在一个对象中，方便检索
dictionary = {'LR': vectorizer_tfidf_DR, 'LR_VDA': vectorizer_tfidf_VDA_DRC}
algorithm = {'LR': lr, 'LR_VDA': lr_vda}


# 获取某case属于某类的概率最高的n个下标
def GetTopNProba(predict_proba, n_length):
    top = []
    p = predict_proba.copy()
    for i in range(n_length):
        top.append(p.index(max(p)))
        p[top[-1]] = 0
    return top


# 将获取的下标与类型列表相匹配，得到其名称


def GetTopNClassifyNameOnePiece(predict_proba, classes, n):
    classnames_proba = []
    p = predict_proba.copy().tolist()[0]
    name_index = GetTopNProba(p, n)
    for i in name_index:
        classnames_proba.append([classes[i], p[i]])
    return classnames_proba


def GetTopNClassifyNameManyPiece(predict_proba, classes, n):
    classnames_proba = []
    p = predict_proba.copy().tolist()
    for k in range(len(p)):
        name_index = GetTopNProba(p[k], n)
        name_proba = []
        for i in name_index:
            name_proba.append([classes[i], p[i]])
        classnames_proba.append(name_proba)
    return classnames_proba


def BinaryClassifyVDA(input_text, algorithm_type='LR_VDA', dictionary_type='LR_VDA'):
    text_tfidf = dictionary[dictionary_type].transform(input_text)
    proba = algorithm[algorithm_type].predict_proba(text_tfidf).copy().tolist()[0]
    classes = algorithm[algorithm_type].classes_.copy().tolist()
    result = algorithm[algorithm_type].predict(text_tfidf)[0]
    other = abs(classes.index(result) - 1)
    return [[result, proba[classes.index(result)]], [classes[other], proba[other]], ['null', 0.0]]


# 接收并返回多条text的结果(未完成)
# def ClassifyMany(input_text, algorithm_type='LR',n=3):
# if type(input_text) == type('1'):
#     input_text = [input_text]
# if type(input_text) == type([1]):
#     text_tfidf = vectorizer.transform(input_text)
#     proba = algorithm[algorithm_type].predict_proba(text_tfidf)
#     classes = GetTopNClassifyNameManyPiece(proba, algorithm[algorithm_type].classes_, n)
# else:
#     print('input error. str or list type only!')
#     return
# return {'result':classes}

# 只接收一条text，并返回结果，格式{'first': {'component': 'Database', 'possibility': 0.5}, 'second': {'component': 'Configuration Logging', 'possibility': 0.04}, 'third': {'component': 'Studio', 'possibility': 0.03}}
def ClassifyOne(input_text, algorithm_type='LR', dictionary_type='LR', n=3):
    result = {}
    if isinstance(input_text, str):
        input_text = [input_text]
    if isinstance(input_text, list):
        text_tfidf = dictionary[dictionary_type].transform(input_text)
        proba = algorithm[algorithm_type].predict_proba(text_tfidf)
        classes_proba = GetTopNClassifyNameOnePiece(
            proba, algorithm[algorithm_type].classes_, n)
        classes_proba_sort = sorted(
            classes_proba, key=lambda x: x[1], reverse=True)
        if classes_proba_sort[0][1] < 0.2 and abs(classes_proba_sort[0][1] - classes_proba_sort[1][1]) < 0.1:
            classes_proba_sort = BinaryClassifyVDA(input_text)
        rank = ['first', 'second', 'third']
        if n <= 3:
            for i, j in zip(classes_proba_sort, rank[:n]):
                result[j] = {'component': i[0], 'possibility': i[1]}
        else:
            for i, j in zip(classes_proba_sort, [x + 1 for x in range(n)]):
                result[j] = {'component': i[0], 'possibility': i[1]}
    return result


def ClassifyOneWithListOutput(input_text, algorithm_type='LR', dictionary_type='LR', n=3):
    result = []
    if isinstance(input_text, str):
        input_text = [input_text]
    if isinstance(input_text, list):
        text_tfidf = dictionary[dictionary_type].transform(input_text)
        proba = algorithm[algorithm_type].predict_proba(text_tfidf)
        classes_proba = GetTopNClassifyNameOnePiece(
            proba, algorithm[algorithm_type].classes_, n)
        classes_proba_sort = sorted(
            classes_proba, key=lambda x: x[1], reverse=True)
        if classes_proba_sort[0][1] < 0.2 and abs(classes_proba_sort[0][1] - classes_proba_sort[1][1]) < 0.1:
            classes_proba_sort = BinaryClassifyVDA(input_text)
        for i, j in zip(classes_proba_sort, [x + 1 for x in range(n)]):
            result.append({'component': i[0], 'possibility': i[1]})
    return result


if __name__ == '__main__':
    text = 'w3p process is consuming GBs of Ram every couple of days. Customer restarts the IIS server to get this resolved. The issue seems to me just the size of the environment and metrics data causing the issue for IIS.'
    print(ClassifyOne(text))