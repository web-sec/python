class fibo(object):
    def __getitem__(self, item):
        if item == 0 or item == 1:
            return 1
        else:
            a=1
            b=1
            for i in range(item-1):
                a, b = b, a + b
            return b

f = fibo()
for i in range(15):
    print(f[i])