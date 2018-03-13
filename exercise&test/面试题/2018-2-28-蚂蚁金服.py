#encoding:utf-8
#输入字符串s,求该字符串的ngram(n-1),比如s=abcdef,ngram(s,3)=[ab,bc,cd,de,ef]
def NGram(s,n=3):
    ngrams = []
    if len(s) >= n-1:
        for i in range(len(s)-(n-1)):
            ngrams.append(s[i:i+2])
    return ngrams

print(NGram('abcdefg',3))
