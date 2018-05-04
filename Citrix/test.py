def GetTopNProba(predict_proba,n_length):
    top = []
    p = predict_proba.copy()
    for i in range(n_length):
        top.append(p.index(max(p)))
        p[top[-1]] = 0
    return top


a = [1,3,4,5,6,7,2,34537,45,7542,]
print(GetTopNProba(a,3))
print(a)